<script setup>
import { RouterLink } from 'vue-router';
import { useI18n } from 'vue-i18n';

const { t } = useI18n();
</script>

<template>
  <div class="landing-container">
    <div class="content-box">
      <h1 class="landing-title">{{ t('landingTitle') }}</h1>
      <p class="landing-subtitle">{{ t('landingSubtitle') }}</p>
      <div class="landing-info">
        <p>{{ t('landingInfo') }}</p>
      </div>
      <router-link to="/menu" class="start-button">
        {{ t('startButton') }}
      </router-link>
    </div>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
  --bg-color: #0b0d10;
  --panel-bg: #1a202c;
  --box-bg: rgba(26, 32, 44, 0.7);
  --text-color: #e2e8f0;
  --muted-text: #a0aec0;
  --highlight-color: #6366f1;
  --button-hover: #4338ca;
  --error-color: #f87171;
  --border-color: #4a5568;
  --shadow-color: #0d1217;
}
.app-container {
  background-color: var(--bg-color);
  background-image: radial-gradient(at 0% 0%, rgba(99, 102, 241, 0.15), transparent 50%),
                    radial-gradient(at 100% 100%, rgba(99, 102, 241, 0.15), transparent 50%);
  background-attachment: fixed;
  background-size: cover;
  min-height: 100vh;
}


.landing-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  min-height: 100vh;
 
  background-attachment: fixed;
  background-size: cover;
  color: var(--text-color);
  padding: 1rem;
  text-align: center;
  font-family: 'Inter', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

.content-box {
  background-color: var(--box-bg);
  backdrop-filter: blur(10px);
  padding: 3rem;
  border-radius: 1.5rem;
  box-shadow: 
    0 25px 50px -12px rgba(0, 0, 0, 0.25),
    0 8px 15px -3px rgba(0, 0, 0, 0.1),
    inset 0 1px 0 rgba(255, 255, 255, 0.05);
  max-width: 600px;
  width: 100%;
  border: 1px solid var(--border-color);
  transition: all 0.3s ease;
}

.landing-title {
  font-size: 2.5rem;
  font-weight: 800;
  color: var(--highlight-color);
  margin-bottom: 1rem;
  letter-spacing: -0.05em;
  text-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
}

.landing-subtitle {
  font-size: 1.25rem;
  color: var(--muted-text);
  margin-bottom: 2rem;
  line-height: 1.5;
}

.landing-info {
  margin-bottom: 2rem;
  color: var(--muted-text);
  line-height: 1.6;
}

.text-limit {
  font-style: italic;
  font-size: 0.9rem;
  color: var(--error-color);
  margin-top: 0.5rem;
}

.start-button {
  display: inline-block;
  padding: 1rem 2.5rem;
  background-color: #393a83;
  color: var(--text-color);
  border-radius: 9999px;
  text-decoration: none;
  font-weight: 700;
  transition: all 0.3s ease;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

.start-button:hover {
  background-color: #4338ca;
  transform: translateY(-2px);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05), 0 0 20px rgba(99, 102, 241, 0.5);
}

.start-button:active {
  transform: translateY(1px);
  box-shadow: 0 2px 4px -1px rgba(0, 0, 0, 0.1), inset 0 2px 4px rgba(0, 0, 0, 0.2);
}
</style>
