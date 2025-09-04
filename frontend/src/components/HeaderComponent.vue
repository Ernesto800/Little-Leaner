<script setup>
import { useI18n } from 'vue-i18n';
import { RouterLink } from 'vue-router';

const { locale } = useI18n();
</script>

<template>
  <header class="app-header">
    <RouterLink to="/" class="app-title-link">
      <h1 class="app-title">
        Little Learner
      </h1>
    </RouterLink>

    <div class="language-selector-container">
      <select v-model="locale" class="language-selector">
        <option value="es">Español</option>
        <option value="en">English</option>
      </select>
    </div>
  </header>
</template>

<style scoped>
.app-header {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  z-index: 1000;

  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.0rem;
  box-sizing: border-box;
  margin: 0px 0 !important;
  background-color: #ffffff;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  text-align: center;
  color: #333;
  font-size: 2.5rem;
  font-weight: 800;
  animation: slideInFromTop 0.5s ease-out;
}

.app-title-link {
  text-decoration: none;
}

.app-title {
  color: #333;
  font-size: 1.5rem;
  font-weight: 800;
  animation: slideInFromTop 0.5s ease-out;
  text-align: start;
  width: 100%;
}

.language-selector-container {
  display: flex;
  position: relative;
}

.language-selector {
  background-color: #374151;
  color: #fff;
  padding: 0.5rem 1rem;
  width: 100px;
  border-radius: 9999px;
  border: 1px solid #374151;
  font-size: 0.8rem;
  cursor: pointer;
  -webkit-appearance: none;
  -moz-appearance: none;
  appearance: none;
  background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="white"><path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd" /></svg>');
  background-repeat: no-repeat;
  background-position: right 0.75rem center;
  background-size: 1.25rem 1.25rem;
  outline: none;
  transition: all 0.3s ease-in-out;
  margin-right: 30px;
}

.language-selector:focus {
  border-color: #3b82f6;
  box-shadow: 0 0 0 2px #3b82f6;
}

@keyframes slideInFromTop {
  from {
    transform: translateY(-50px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

@media (max-width: 640px) {
  .app-header {
    flex-direction: column;
    gap: 1rem;
    padding-top: calc(1rem + 20px);
    padding-bottom: 1rem;
  }

  .app-title {
    font-size: 2rem;
  }
}
</style>
