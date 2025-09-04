<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue';
import { useI18n } from 'vue-i18n';
import { useRouter } from 'vue-router';

const { t, locale } = useI18n();
const router = useRouter();

const themeInput = ref('');
const languageSelect = ref(locale.value);
const placeholderIndex = ref(0);
const placeholderText = ref('');
let intervalId = null;

const isButtonDisabled = computed(() => {
  return !themeInput.value.trim();
});

const navigateToLesson = () => {
  if (isButtonDisabled.value) return;
  router.push({
    name: 'tinylessoninside',
    params: {
      theme: themeInput.value.trim(),
      language: languageSelect.value,
    },
  });
};

const placeholderExamples = computed(() => {
  if (locale.value === 'es') {
    return [
      "Jugar videojuegos",
      "Ir a cenar en familia",
      "Crear una receta de cocina",
      "Aprender a pintar",
      "Preparar un viaje de mochilero"
    ];
  } else {
    return [
      "Playing video games",
      "Going to a family dinner",
      "Creating a cooking recipe",
      "Learning to paint",
      "Preparing a backpacking trip"
    ];
  }
});

const updatePlaceholder = () => {
  const examples = placeholderExamples.value;
  placeholderIndex.value = (placeholderIndex.value + 1) % examples.length;
  placeholderText.value = examples[placeholderIndex.value];
};

const startPlaceholderInterval = () => {
  clearInterval(intervalId);
  placeholderText.value = placeholderExamples.value[0];
  intervalId = setInterval(updatePlaceholder, 3000);
};

onMounted(() => {
  startPlaceholderInterval();
});

onUnmounted(() => {
  clearInterval(intervalId);
});

watch(locale, () => {
  startPlaceholderInterval();
});
</script>

<template>
  <div class="main-container">
    <div class="content-wrapper">
      <div class="text-section">
        <h1 class="title">{{ t('tinyLesson.title') }}</h1>
        <p class="subtitle">{{ t('tinyLesson.subtitle') }}</p>
      </div>

      <div class="form-section">
        <div class="form-group">
          <label for="theme" class="label">{{ t('tinyLesson.purposeOrTheme') }}</label>
          <div class="input-container">
            <input
              type="text"
              id="theme"
              class="input"
              v-model="themeInput"
            />
            
            <transition name="placeholder-fade" mode="out-in">
              <span v-if="!themeInput" :key="placeholderIndex" class="placeholder-text">{{ placeholderText }}</span>
            </transition>
          </div>
        </div>

        
        <button
          @click="navigateToLesson"
          class="generate-button"
          :disabled="isButtonDisabled"
        >
          {{ t('tinyLesson.generateButton') }}
          <svg class="arrow-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M5 12H19" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M12 5L19 12L12 19" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </button>
      </div>
    </div>
  </div>
</template>


<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700;800&display=swap');

.main-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  width: 100vw;
  background-color: #1a1a1a;
  font-family: 'Inter', sans-serif;
  color: #fff;
  padding: 1rem;
}

.content-wrapper {
  background-color: #282828;
  padding: 3rem 2rem;
  border-radius: 1rem;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
  max-width: 500px;
  width: 100%;
  text-align: center;
}

.text-section {
  margin-bottom: 2rem;
}

.title {
  font-size: 2.5rem;
  font-weight: 800;
  margin: 0 0 0.5rem 0;
  color: #fff;
}

.subtitle {
  font-size: 1.1rem;
  font-weight: 400;
  color: #a0a0a0;
  margin: 0;
}

.form-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1.5rem;
}

.form-group {
  width: 100%;
}

.label {
  display: block;
  text-align: left;
  font-size: 0.8rem;
  font-weight: 600;
  color: #a0a0a0;
  text-transform: uppercase;
  margin-bottom: 0.5rem;
  letter-spacing: 1px;
}

.input {
  width: 100%;
  padding: 0.75rem 1rem;
  font-size: 1rem;
  color: #fff;
  background-color: #383838;
  border: 1px solid #444;
  border-radius: 0.5rem;
  box-sizing: border-box;
  transition: border-color 0.2s;
}

.input::placeholder {
  color: #666;
}

.input:focus {
  outline: none;
  border-color: #3b82f6;
}

.generate-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  padding: 0.75rem 2.5rem;
  font-size: 1rem;
  font-weight: 600;
  color: #fff;
  background-color: #3b82f6;
  border: none;
  border-radius: 9999px;
  cursor: pointer;
  transition: background-color 0.2s ease-in-out, transform 0.2s ease-in-out;
  box-shadow: 0 5px 15px rgba(59, 130, 246, 0.2);
}

.generate-button:hover:not([disabled]) {
  background-color: #2563eb;
  transform: translateY(-2px);
}

.generate-button:active:not([disabled]) {
  transform: translateY(0);
  box-shadow: 0 2px 10px rgba(59, 130, 246, 0.3);
}

.generate-button[disabled] {
  opacity: 0.5;
  cursor: not-allowed;
}

.arrow-icon {
  width: 1.25rem;
  height: 1.25rem;
  transition: transform 0.2s ease-in-out;
}

.generate-button:hover:not([disabled]) .arrow-icon {
  transform: translateX(5px);
}

@media (max-width: 600px) {
  .content-wrapper {
    padding: 2rem 1.5rem;
  }

  .title {
    font-size: 2rem;
  }

  .subtitle {
    font-size: 1rem;
  }
}

.input-container {
  position: relative;
  width: 100%;
}

.placeholder-text {
  position: absolute;
  top: 50%;
  left: 1rem;
  transform: translateY(-50%);
  font-size: 1rem;
  color: #666;
  pointer-events: none;
}

.placeholder-fade-enter-active,
.placeholder-fade-leave-active {
  transition: opacity 0.5s ease-in-out;
}

.placeholder-fade-enter-from,
.placeholder-fade-leave-to {
  opacity: 0;
}
</style>
