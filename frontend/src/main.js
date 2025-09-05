import { createApp } from 'vue';
import { createI18n } from 'vue-i18n';
import App from './App.vue';
import router from './router';

import es from './traductions/es.json';
import en from './traductions/en.json';

const i18n = createI18n({
  locale: 'es',
  legacy: false,
  fallbackLocale: 'en',
  messages: {
    es,
    en
  }
});

const app = createApp(App);
app.use(router);
app.use(i18n);

app.mount('#app');
