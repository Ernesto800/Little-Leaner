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
      en: {} 
    }
  });

  try {
    const esMessages = await import('./traductions/es.json?url').then(m => fetch(m.default).then(r => r.json()));
    i18n.global.setLocaleMessage('es', esMessages);
  } catch (error) {
    console.error('No se pudo cargar la traducción', error);
  }

  const app = createApp(App);
  app.use(router);
  app.use(i18n);

  app.mount('#app');
}

setupApp();
