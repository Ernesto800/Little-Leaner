import { createApp } from 'vue';
import { createI18n } from 'vue-i18n';
import App from './App.vue';
import router from './router';

async function setupApp() {
  const messages = await fetch('/traductions/es.json')
    .then(response => response.json())
    .then(es => ({
      es,
      en: {} 
    }));

  const i18n = createI18n({
    locale: 'es',
    legacy: false,
    fallbackLocale: 'en',
    messages,
  });

  const app = createApp(App);
  app.use(router);
  app.use(i18n);

  app.mount('#app');
}

setupApp();