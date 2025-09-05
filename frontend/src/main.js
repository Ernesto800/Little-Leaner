import { createApp } from 'vue';
import { createI18n } from 'vue-i18n';
import App from './App.vue';
import router from './router';

async function setupApp() {
  const i18n = createI18n({
    locale: 'es',
    legacy: false,
    fallbackLocale: 'en',
    messages: {
      es: {},
      en: {}
    }
  });

  try {
    const response = await fetch('/traductions/es.json');
    if (response.ok) {
      const messages = await response.json();
      i18n.global.setLocaleMessage('es', messages);
    } else {
      console.error('Error al cargar la traducción:', response.statusText);
    }
  } catch (error) {
    console.error('No se pudo cargar la traducción', error);
  }

  const app = createApp(App);
  app.use(router);
  app.use(i18n);

  app.mount('#app');
}

setupApp();