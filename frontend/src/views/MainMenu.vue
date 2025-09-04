<script setup>
import { RouterLink } from 'vue-router'
import { useI18n } from 'vue-i18n';

const { t } = useI18n();
</script>

<template>
  <div class="main-hub-container">
    <div class="left-panel">
      <div class="intro-section">
        <h1 class="title">Little <span class="gemini-text">Language</span><br>Lessons</h1>
        <p class="subtitle">{{ t('mainHub.subtitle') }}</p>
      </div>
    </div>

    <div class="right-panel">
      <div class="lessons-container">
        <div class="lessons-grid">
          <div class="card">
            <h2 class="card-title">{{ t('mainHub.experiment1.title') }}</h2>
            <p class="card-subtitle">{{ t('mainHub.experiment1.subtitle') }}</p>
            <router-link to="/chat" class="start-button">
              {{ t('mainHub.experiment1.button') }}
              <svg class="arrow-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M5 12H19" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M12 5L19 12L12 19" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </router-link>
          </div>

          <div class="card">
            <h2 class="card-title">{{ t('mainHub.experiment2.title') }}</h2>
            <p class="card-subtitle">{{ t('mainHub.experiment2.subtitle') }}</p>
            <router-link to="/tinylesson" class="start-button">
              {{ t('mainHub.experiment2.button') }}
              <svg class="arrow-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M5 12H19" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M12 5L19 12L12 19" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </router-link>
          </div>

          <div class="card">
            <h2 class="card-title">{{ t('mainHub.experiment3.title') }}</h2>
            <p class="card-subtitle">{{ t('mainHub.experiment3.subtitle') }}</p>
            <router-link to="/pronouncepractice" class="start-button">
              {{ t('mainHub.experiment3.button') }}
              <svg class="arrow-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M5 12H19" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M12 5L19 12L12 19" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700;800&display=swap');

.main-hub-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  width: 100%;
  margin-top: 6.0rem;
  max-width: auto;
  background-color: #f7f7f7;
  font-family: 'Inter', sans-serif;
  gap: 4rem;
  padding: 4rem;
  overflow: hidden;
}

.left-panel {
  width: 100%;
  max-width: 400px;
  align-self: flex-start;
  position: sticky;
  top: 4rem;
  height: 100vh;
  padding-right: 100px;
}

.right-panel {
  width: 100%;
  max-width: 800px;
  overflow-y: auto;
  height: 100vh;
  padding-right: 30px;
  margin-left: auto;
}

.intro-section {
  width: 100%;
  text-align: left;
  margin-left: 18rem;
  margin-top: 8rem;
}

.title {
  font-size: 4rem;
  font-weight: 800;
  width: 32rem;
  color: #333;
  margin: 0;
  line-height: 1.1;
  text-align: center;
}

.gemini-text {
  color: #3b82f6;
}

.subtitle {
  font-size: 1.125rem;
  color: #666;
  width: 24rem;
  position: relative;
  top: 2rem;
  left: 3.2rem;
  font-weight: 500;
  text-align: center;
}

.lessons-container {
  width: 100%;
}

.lessons-grid {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  width: 100%;
}

.card {
  background-color: #ffffff;
  border-radius: 1rem;
  padding: 1.5rem 2rem;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
  border: 1px solid #e0e0e0;
  position: relative;
  overflow: hidden;
  height: 16rem;
}

.experiment-number {
  font-size: 0.75rem;
  font-weight: 600;
  color: #3b82f6;
  margin: 0;
  text-transform: uppercase;
}

.card-title {
  font-size: 3rem;
  font-weight: 700;
  color: #333;
  margin: 0.5rem 0 0.5rem 0;
  line-height: 1.1;
}

.card-subtitle {
  font-size: 1.2rem;
  position: relative;
  top: 1rem;
  color: #666;
  width: 34rem;
}

.start-button {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  font-weight: 600;
  color: #3b82f6;
  background-color: transparent;
  border: 2px solid #3b82f6;
  border-radius: 9999px;
  text-decoration: none;
  transition: all 0.2s ease-in-out;
  position: relative;
  top: 4rem;
}

.start-button:hover {
  background-color: #3b82f6;
  color: #fff;
  cursor: pointer;
}


.arrow-icon {
  width: 1.25rem;
  height: 1.25rem;
  transition: transform 0.2s ease-in-out;
}

.start-button:hover:not(.disabled-button) .arrow-icon {
  transform: translateX(5px);
}

.card-image {
  position: absolute;
  top: 50%;
  right: 1.5rem;
  transform: translateY(-50%);
  width: 120px;
  height: auto;
}

@media (max-width: 768px) {
  .main-hub-container {
    flex-direction: column;
    padding: 2rem;
    gap: 2rem;
  }
  .left-panel {
    position: relative;
    top: auto;
    align-self: auto;
    height: auto;
  }
  .intro-section {
    margin: 0 auto;
    text-align: center;
  }
  .right-panel {
    height: auto;
    overflow-y: visible;
  }
  .lessons-grid {
    padding: 0;
  }
  .card-image {
    display: none;
  }
}
</style>
