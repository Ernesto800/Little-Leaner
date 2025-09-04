<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import { useI18n } from "vue-i18n";

const props = defineProps<{
  theme: string;
  language: string;
}>();

const { t } = useI18n({
  messages: {
    en: {
      tinyLessonInside: {
        seeLess: 'See less',
        seeMore: 'See more',
        vocabularyTab: 'Vocabulary',
        phrasesTab: 'Phrases',
        generateContent: 'Generate Content',
      },
    },
    es: {
      tinyLessonInside: {
        seeLess: 'Ver menos',
        seeMore: 'Ver más',
        vocabularyTab: 'Vocabulario',
        phrasesTab: 'Frases',
        generateContent: 'Generar Contenido',
      },
    },
  },
});

const showAll = ref(false);
const showMoreText = computed(() => {
  return showAll.value ? t("tinyLessonInside.seeLess") : t("tinyLessonInside.seeMore");
});

const activeTab = ref("vocabularyTab");

const isLoading = ref(false);
const hasGenerated = ref(false);
const error = ref<string | null>(null);

const content = ref<{ vocabulary?: { word: string; translation: string; }[]; phrases?: { phrase: string; translation: string; }[]; } | null>(null);

async function generate() {
  isLoading.value = true;
  hasGenerated.value = true;
  content.value = null;
  error.value = null;

  try {
    let prompt;
    if (props.language === 'en') {
      prompt = `Generate vocabulary and phrases for the theme "${props.theme}". Generate all content in English. The format must be a single JSON object with two arrays: 'vocabulary' (20 objects with 'word' and 'translation') and 'phrases' (10 objects with 'phrase' and 'translation').`;
    } else {
      prompt = `Genera vocabulario y frases para el tema "${props.theme}". Genera todo el contenido en español. El formato debe ser un único objeto JSON con dos arrays: 'vocabulary' (20 objetos con 'word' y 'translation') y 'phrases' (10 objetos con 'phrase' y 'translation').`;
    }
    
    const response = await fetch('http://localhost:5000/api/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ prompt: prompt, history: [] }),
    });

    if (!response.ok) {
      throw new Error(`Error en el servidor: ${response.status}`);
    }

    const result = await response.json();
    content.value = result.message;
    

  } catch (err) {
    console.error('Error al generar el contenido:', err);
    error.value = "Error de conexión: No se pudo conectar con el servidor. Asegúrate de que el backend está en funcionamiento.";
  } finally {
    isLoading.value = false;
  }
}

onMounted(() => {
  generate();
});
</script>

<template>
  <div class="main-container">
    <div class="header-section">
      <h1 class="main-title">
        <span class="theme-highlight">{{ props.theme }}</span>
      </h1>
      <button @click="generate" class="generate-button">
        {{ t('tinyLessonInside.generateContent') }}
      </button>
    </div>

    <div class="tab-container">
      <button
        @click="activeTab = 'vocabularyTab'"
        class="tab-button"
        :class="{ 'tab-active': activeTab === 'vocabularyTab' }"
      >
        {{ t('tinyLessonInside.vocabularyTab') }}
      </button>
      <button
        @click="activeTab = 'phrasesTab'"
        class="tab-button"
        :class="{ 'tab-active': activeTab === 'phrasesTab' }"
      >
        {{ t('tinyLessonInside.phrasesTab') }}
      </button>
    </div>

    <div class="content-section">
      <div v-if="activeTab === 'vocabularyTab'">
        <div v-if="content && content.vocabulary" class="content-wrapper">
          <div class="vocabulary-grid">
            <div
              v-for="(item, index) in (showAll ? content.vocabulary : content.vocabulary.slice(0, 8))"
              :key="index"
              class="vocabulary-card"
            >
              <div>
                <h3 class="card-word">{{ item.word }}</h3>
                <p class="card-translation">{{ item.translation }}</p>
              </div>
            </div>
          </div>
        </div>
        <div v-else-if="isLoading" class="loading-container">
          <div class="spinner"></div>
          <p>Generando contenido...</p>
        </div>
        <div v-else-if="error" class="error-container">
          <p>{{ error }}</p>
        </div>
        <div v-else class="empty-state">
          <p>Haz clic en el botón de generar para crear contenido.</p>
        </div>
      </div>
      <div v-if="activeTab === 'phrasesTab'">
        <div v-if="content && content.phrases" class="content-wrapper">
          <div class="phrases-list">
            <div v-for="(item, index) in content.phrases" :key="index" class="phrase-card">
              <h3 class="card-word">{{ item.phrase }}</h3>
              <p class="card-translation">{{ item.translation }}</p>
            </div>
          </div>
        </div>
        <div v-else class="empty-state">
          <p>No hay frases para mostrar. Haz clic en el botón de generar para crear contenido.</p>
        </div>
      </div>
    </div>

    <div class="footer-button-container">
      <button
        v-if="!isLoading && hasGenerated && activeTab === 'vocabularyTab' && !error"
        @click="showAll = !showAll"
        class="show-more-button"
      >
        <span>{{ showMoreText }}</span>
        <svg v-if="!showAll" class="show-more-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M19 9l-7 7-7-7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        <svg v-else class="show-more-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M5 15l7-7 7 7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </button>
    </div>
  </div>
</template>

<style scoped>
:root {
  --background-color: #0d1117;
  --card-background: #161b22;
  --text-color: #c9d1d9;
  --highlight-color: #58a6ff;
  --button-hover: #21262d;
  --border-color: #30363d;
  --gold-accent: #ffd700;
  --font-family: 'Inter', sans-serif;
}

body {
  font-family: var(--font-family);
  background-color: var(--background-color);
  color: var(--text-color);
  margin: 0;
}

.main-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background-color: var(--background-color);
  padding: 2rem;
  box-sizing: border-box;
  margin-top: 8rem;
}

.header-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  gap: 20px;
}

.main-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: var(--text-color);
  text-shadow: 0 0 10px rgba(88, 166, 255, 0.2);
  text-align: left;
}

.theme-highlight {
  color: var(--highlight-color);
  text-transform: capitalize;
}

.generate-button {
  background: linear-gradient(135deg, #58a6ff, #58a6ff);
  color: #0d1117;
  border: none;
  border-radius: 9999px;
  padding: 0.75rem 2rem;
  font-size: 1.1rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(88, 166, 255, 0.4);
}

.generate-button:hover {
  background: linear-gradient(135deg, #4c96e6, #4c96e6);
  box-shadow: 0 6px 20px rgba(88, 166, 255, 0.6);
  transform: translateY(-2px);
}

.tab-container {
  display: flex;
  justify-content: center;
  margin-bottom: 2rem;
  background-color: var(--card-background);
  border-radius: 12px;
  padding: 0.5rem;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.tab-button {
  flex: 1;
  padding: 0.75rem 1.5rem;
  font-size: 1rem;
  font-weight: 600;
  background-color: transparent;
  border: none;
  color: var(--text-color);
  border-radius: 9px;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.1s ease;
  white-space: nowrap;
}

.tab-button:hover {
  background-color: var(--button-hover);
}

.tab-active {
  background: linear-gradient(135deg, #1f2730, #2a313c);
  color: var(--highlight-color);
  box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.3), 0 0 15px rgba(88, 166, 255, 0.15);
}

.content-section {
  flex-grow: 1;
}

.content-wrapper {
  animation: fadeIn 0.8s ease-out;
}

.vocabulary-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.5rem;
}

.vocabulary-card,
.phrase-card {
  background: linear-gradient(145deg, #1b2028, #13171e);
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  border: 1px solid var(--border-color);
  position: relative;
  overflow: hidden;
}

.vocabulary-card:hover,
.phrase-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.4);
}

.vocabulary-card::before,
.phrase-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 5px;
  background: linear-gradient(90deg, #ffd700, #58a6ff);
  transform: translateX(-100%);
  transition: transform 0.6s ease;
}

.vocabulary-card:hover::before,
.phrase-card:hover::before {
  transform: translateX(0);
}

.card-word {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--highlight-color);
  margin-bottom: 0.5rem;
}

.card-translation {
  font-size: 1rem;
  color: var(--text-color);
  opacity: 0.8;
}

.phrases-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.phrase-card {
  padding: 2rem;
}

.loading-container,
.error-container,
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 300px;
  text-align: center;
  color: var(--text-color);
  opacity: 0.6;
}

.spinner {
  border: 4px solid var(--border-color);
  border-top: 4px solid var(--highlight-color);
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

.footer-button-container {
  display: flex;
  justify-content: center;
  padding-top: 2rem;
}

.show-more-button {
  background: var(--card-background);
  color: var(--highlight-color);
  border: 1px solid var(--border-color);
  border-radius: 9999px;
  padding: 0.75rem 1.5rem;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.3s ease;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.show-more-button:hover {
  background: var(--button-hover);
  border-color: var(--highlight-color);
  transform: translateY(-2px);
  box-shadow: 0 6px 12px rgba(88, 166, 255, 0.2);
}

.show-more-icon {
  width: 16px;
  height: 16px;
  transition: transform 0.3s ease;
}

@media (max-width: 640px) {
  .main-title {
    font-size: 2rem;
  }
  .header-section {
    flex-direction: column;
    align-items: flex-start;
  }
  .generate-button {
    margin-top: 1rem;
  }
  .tab-container {
    flex-direction: column;
    padding: 0.5rem;
  }
  .tab-button {
    padding: 0.75rem;
  }
  .vocabulary-grid {
    grid-template-columns: 1fr;
  }
}
</style>
