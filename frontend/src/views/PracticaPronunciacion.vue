<script setup>
import { ref } from "vue";
import { useI18n } from "vue-i18n";

const { t, locale } = useI18n({
  messages: {
    en: {
      analyzer: {
        title: "Text Analyzer",
        instruction: "Enter a sentence in English to analyze.",
        analyzeButton: "Analyze Text",
        analyzing: "Analyzing text...",
        feedbackTitle: "AI Feedback",
        placeholderInput: "Write your sentence here...",
        placeholder: "Your text analysis will appear here.",
        apiError: "Error from AI API. Please try again.",
        noText: "Please enter some text to analyze.",
      },
    },
    es: {
      analyzer: {
        title: "Analizador de Texto",
        instruction: "Introduce una frase en inglés para analizar.",
        analyzeButton: "Analizar Texto",
        analyzing: "Analizando texto...",
        feedbackTitle: "Feedback de la IA",
        placeholderInput: "Escribe tu frase aqui...",
        placeholder: "Tu análisis de texto aparecerá aquí.",
        apiError: "Error de la API de IA. Por favor, inténtalo de nuevo.",
        noText: "Por favor, introduce algún texto para analizar.",
      },
    },
  },
});

const sentence = ref('');
const loading = ref(false);
const feedback = ref(null);
const errorMessage = ref('');

const analyzeText = async () => {
  if (sentence.value.trim() === '') {
    errorMessage.value = t("analyzer.noText");
    return;
  }
  
  loading.value = true;
  feedback.value = null;
  errorMessage.value = '';

  try {
    const response = await fetch('http://localhost:5000/api/analyze_text', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ sentence: sentence.value, language: locale.value })
    });

    if (!response.ok) {
        throw new Error(`Error de la API: ${response.status} ${response.statusText}`);
    }

    const data = await response.json();
    
    if (data.feedback) {
      feedback.value = data.feedback;
      errorMessage.value = '';
    } else {
      throw new Error(data.error || t('analyzer.apiError'));
    }
  } catch (error) {
    errorMessage.value = `Error: ${error.message}`;
    console.error('Error al analizar el texto:', error);
  } finally {
    loading.value = false;
  }
};
</script>

<template>
  <div class="container">
    <div class="main-panel">
      
      <div class="control-panel">
        <h1 class="title">{{ t("analyzer.title") }}</h1>
        
        <div class="action-box">
          <p class="instruction-text">{{ t("analyzer.instruction") }}</p>
          
          <textarea
            v-model="sentence"
            class="text-input"
            rows="5"
            :placeholder="t('analyzer.placeholderInput')"
          ></textarea>
          
          <button
            @click="analyzeText"
            :disabled="loading"
            class="action-button analyze-button"
          >
            <span v-if="loading">{{ t("analyzer.analyzing") }}</span>
            <span v-else>{{ t("analyzer.analyzeButton") }}</span>
          </button>
        </div>
      </div>
      
      <div class="feedback-panel">
        <h2 class="feedback-title">
          {{ t("analyzer.feedbackTitle") }}
        </h2>
        <p v-if="feedback" class="feedback-text">{{ feedback }}</p>
        <p v-else class="placeholder-text">
          {{ t("analyzer.placeholder") }}
        </p>
        <p v-if="errorMessage" class="error-text">{{ errorMessage }}</p>
      </div>
      
    </div>
  </div>
</template>

<style scoped>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
  --bg-color: #0b0d10;
  --panel-bg: #1a202c;
  --box-bg: #2d3748;
  --text-color: #e2e8f0;
  --muted-text: #a0aec0;
  --highlight-color: #6366f1;
  --button-hover: #4338ca;
  --error-color: #f87171;
  --border-color: #4a5568;
  --shadow-color: #0d1217;
}

body {
  margin: 0;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  background-color: var(--bg-color);
  background-image: radial-gradient(at 0% 0%, rgba(99, 102, 241, 0.15), transparent 50%),
                    radial-gradient(at 100% 100%, rgba(99, 102, 241, 0.15), transparent 50%);
  background-attachment: fixed;
  background-size: cover;
  min-height: 100vh;
}


.container {
  min-height: 100vh;
  color: var(--text-color);
  padding: 2rem 1rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  transition: background-color 0.5s ease;
}

.main-panel {
  width: 100%;
  max-width: 76rem;
  background-color: var(--panel-bg);
  border-radius: 1.5rem;
  box-shadow: 
    0 25px 50px -12px rgba(0, 0, 0, 0.25),
    0 8px 15px -3px rgba(0, 0, 0, 0.1),
    inset 0 1px 0 rgba(255, 255, 255, 0.05);
  display: flex;
  flex-direction: column;
  gap: 2rem;
  padding: 2rem 1rem;

  border: 1px solid var(--border-color);
}

@media (min-width: 768px) {
  .main-panel {
    flex-direction: row;
    padding: 3rem;
    gap: 2rem;
    align-items: stretch;
  }
}

.control-panel, .feedback-panel {
  display: flex;
  flex-direction: column;
  gap: 2rem;
  width: 100%;
}

@media (min-width: 768px) {
  .control-panel, .feedback-panel {
    width: 50%;
    min-width: 32rem;
    flex-shrink: 0;
    flex-grow: 1;
  }
}

.title {
  font-size: 2.5rem;
  font-weight: 800;
  color: var(--text-color);
  text-align: center;
  letter-spacing: -0.05em;
  text-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
}

.action-box {
  background-color: var(--box-bg);
  border-radius: 1.5rem;
  box-shadow: inset 0 2px 4px 0 rgba(0, 0, 0, 0.1), 0 10px 15px -3px rgba(0, 0, 0, 0.1);
  padding: 3rem;
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 1.5rem;
  border: 1px solid var(--border-color);
  position: relative;
  overflow: hidden;
}

.instruction-text {
  font-size: 1rem;
  color: var(--muted-text);
  margin-bottom: 0.5rem;
  text-align: center;
  line-height: 1.5;
}

.text-input {
  width: 100%;
  padding: 1.25rem;
  border-radius: 1rem;
  border: 1px solid var(--border-color);
  background-color: var(--panel-bg);
  color: var(--text-color);
  font-family: inherit;
  resize: none;
  min-height: 10rem;
  box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.2);
  transition: all 0.3s ease;
}

.text-input:focus {
  outline: none;
  border-color: var(--highlight-color);
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.25);
}

.action-button {
  width: 100%;
  padding: 1.25rem;
  border-radius: 1rem;
  font-weight: 700;
  transition: all 0.3s ease;
  transform: scale(1);
  border: none;
  cursor: pointer;
  color: var(--text-color);
  background: var(--highlight-color);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

.action-button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05), 0 0 20px rgba(99, 102, 241, 0.5);
  background: var(--button-hover);
}

.action-button:active:not(:disabled) {
  transform: translateY(1px);
  box-shadow: 0 2px 4px -1px rgba(0, 0, 0, 0.1), inset 0 2px 4px rgba(0, 0, 0, 0.2);
}

.action-button:disabled {
  background-color: var(--border-color);
  color: #718096;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.analyze-button {
  background-color: var(--highlight-color);
}

.feedback-panel {
  background-color: var(--box-bg);
  border-radius: 1.5rem;
  box-shadow: inset 0 2px 4px 0 rgba(0, 0, 0, 0.1), 0 10px 15px -3px rgba(0, 0, 0, 0.1);
  padding: 1rem;
  flex-grow: 1;
  overflow-y: auto;
  border: 1px solid var(--border-color);
  display: flex;
  flex-direction: column;
  width: 20px;
}

.feedback-title {
  font-size: 1.75rem;
  font-weight: 700;
  color: var(--text-color);
  margin-bottom: 1rem;
  border-bottom: 2px solid var(--highlight-color);
  padding-bottom: 0.5rem;
  letter-spacing: -0.025em;
}

.feedback-text {
  color: var(--muted-text);
  line-height: 1.75;
  white-space: pre-wrap;
}

.placeholder-text {
  color: var(--muted-text);
  font-style: italic;
  text-align: center;
  padding: 2rem;
}

.error-text {
  color: var(--error-color);
  margin-top: 1rem;
  text-align: center;
  font-weight: 600;
}

.feedback-panel::-webkit-scrollbar {
  width: 8px;
}

.feedback-panel::-webkit-scrollbar-track {
  background: var(--panel-bg);
  border-radius: 10px;
}

.feedback-panel::-webkit-scrollbar-thumb {
  background-color: var(--muted-text);
  border-radius: 10px;
  border: 2px solid var(--panel-bg);
}

.feedback-panel::-webkit-scrollbar-thumb:hover {
  background-color: var(--highlight-color);
}
</style>
