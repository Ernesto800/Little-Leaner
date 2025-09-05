import { createApp } from 'vue';
import { createI18n } from 'vue-i18n';
import App from './App.vue';
import router from './router';

const messages = Object.fromEntries(
  Object.entries(import.meta.glob('./traductions/*.json', { eager: true }))
    .map(([key, value]) => {
      const locale = key.split('/').pop().replace('.json', '');
      return [locale, value.default];
    })
);

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
