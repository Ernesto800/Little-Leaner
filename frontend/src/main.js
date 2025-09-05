import { createApp } from 'vue';
import { createI18n } from 'vue-i18n';
import App from './App.vue';
import router from './router';

import esMessages from './traductions/es.json';

const i18n = createI18n({
  locale: 'es',
  legacy: false,
  fallbackLocale: 'en',
  messages: {
    es: esMessages,
    en: {}
  }
});

const app = createApp(App);
app.use(router);
app.use(i18n);

app.mount('#app');