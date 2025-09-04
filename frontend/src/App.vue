<script setup>
import { RouterView } from 'vue-router'
import HeaderComponent from './components/HeaderComponent.vue';

</script>

<template>
  <div class="app-container">
    <HeaderComponent/>
    <RouterView />
  </div>
</template>

<style>
:root {
  --color-dark-background: #111827;
  --color-border: #374151;
}

body {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

  .app-container {
    background-color: var(--color-dark-background);
    min-height: 100vh;
    min-width: 100vw;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 2rem 1rem;
    color: #fff;
    box-sizing: border-box;
    padding: 0px !important;
  }
</style>