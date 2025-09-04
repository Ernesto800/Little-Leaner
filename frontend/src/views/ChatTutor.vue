<script setup>
import { ref, watch, nextTick } from 'vue';
import { useI18n } from 'vue-i18n';

const { t, locale } = useI18n();

const messages = ref([]);
const userInput = ref('');
const isSending = ref(false);
const conversationArea = ref(null);
let chatHistory = [];

const scrollToBottom = async () => {
  await nextTick();
  if (conversationArea.value) {
    conversationArea.value.scrollTop = conversationArea.value.scrollHeight;
  }
};

const resetChat = async (newLocale) => {
  console.log(`Cambiando a idioma: ${newLocale}`);
  messages.value = [{
    text: t('initialMessage'),
    sender: 'bot'
  }];
  chatHistory = [{
    role: 'model',
    parts: [{ text: t('initialMessage') }]
  }];
  await scrollToBottom();
};

watch(locale, resetChat, { immediate: true });

const sendMessage = async () => {
  const userMessage = userInput.value.trim();
  if (!userMessage || isSending.value) return;

  messages.value.push({ text: userMessage, sender: 'user' });
  userInput.value = '';
  isSending.value = true;
  scrollToBottom();

  messages.value.push({ text: t('typing'), sender: 'bot', isTyping: true });
  scrollToBottom();

  chatHistory.push({ role: 'user', parts: [{ text: userMessage }] });

  try {
    const apiInstructions = t('apiInstructions');
    const apiKey = "AIzaSyAsc3xmgz2WdIx9m-_i0T6K5czSjU3xkZ8";
    const apiUrl = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key=${apiKey}`;

    const payload = {
      contents: chatHistory,
      systemInstruction: {
        parts: [{ text: apiInstructions }]
      },
    };

    const response = await fetch(apiUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload)
    });

    const result = await response.json();
    const aiResponse = result.candidates?.[0]?.content?.parts?.[0]?.text;

    messages.value.pop();
    if (aiResponse) {
      messages.value.push({ text: aiResponse, sender: 'bot' });
      chatHistory.push({ role: 'model', parts: [{ text: aiResponse }] });
    } else {
      messages.value.push({ text: t('error'), sender: 'bot' });
    }
  } catch (error) {
    console.error('Error al obtener la respuesta de la IA:', error);
    messages.value.pop();
    messages.value.push({ text: t('error'), sender: 'bot' });
  } finally {
    isSending.value = false;
    scrollToBottom();
  }
};
</script>

<template>
  <div class="app-container">
    <div class="chat-container">
      
      <header class="header-text">
        <h1 class="title">{{ t('title') }}</h1>
        <p class="subtitle">{{ t('subtitle') }}</p>
      </header>

      <main class="conversation-area" ref="conversationArea">
        <div 
          v-for="(message, index) in messages" 
          :key="index" 
          :class="['message-wrapper', { 'message-user': message.sender === 'user', 'message-bot': message.sender === 'bot' }]">
          <div :class="['message-bubble', { 'bubble-user': message.sender === 'user', 'bubble-bot': message.sender === 'bot' }]">
            <div v-if="message.isTyping" class="dot-typing-wrapper">
              <div class="dot-typing"></div>
            </div>
            <p v-else>{{ message.text }}</p>
          </div>
        </div>
      </main>

      <footer class="input-area">
        <input 
          v-model="userInput" 
          @keyup.enter="sendMessage()" 
          type="text" 
          :placeholder="t('placeholder')" 
          class="text-input"
          :disabled="isSending"
        />
        <button @click="sendMessage()" :disabled="!userInput.trim() || isSending" class="send-button">
          <svg class="send-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M22 2L11 13M22 2L15 22L11 13L2 9L22 2Z"></path>
          </svg>
        </button>
      </footer>
    </div>
  </div>
</template>


<style scoped>

*, *::before, *::after {
  box-sizing: border-box;
}

:root {
  --color-dark-background: #0b0d10;
  --color-card-background: #1a202c;
  --color-border: #4a5568;
  --color-primary: #6366f1;
  --color-primary-hover: #4338ca;
  --color-accent-blue: #3b82f6;
  --color-user-bubble: #6366f1;
  --color-bot-bubble: #2d3748;
  --color-text-white: #e2e8f0;
  --color-text-muted: #a0aec0;
  --color-title: #6366f1;
  --color-send-button-gradient-start: #6366f1;
  --color-send-button-gradient-end: #8b5cf6;
}

body {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  background-color: var(--color-dark-background);
  color: var(--color-text-white);
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
}

.app-container {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  max-width: 100%;
  min-height: 100vh;
  padding: 0 !important;
  background-color: var(--color-dark-background);
  background-image: radial-gradient(at 0% 0%, rgba(99, 102, 241, 0.15), transparent 50%),
                    radial-gradient(at 100% 100%, rgba(99, 102, 241, 0.15), transparent 50%);
  background-attachment: fixed;
  background-size: cover;
  overflow-x: hidden;
}

.chat-container {
  width: 90%;
  max-width: 42rem;
  height: auto;
  min-height: 720px;
  max-height: 80vh;
  background-color: var(--color-card-background);
  border-radius: 1.5rem;
  box-shadow: 
    0 25px 50px -12px rgba(0, 0, 0, 0.25),
    0 8px 15px -3px rgba(0, 0, 0, 0.1),
    inset 0 1px 0 rgba(255, 255, 255, 0.05);
  display: flex;
  flex-direction: column;
  padding: 1.5rem;
  overflow: hidden;
  position: relative;
  z-index: 10;
  margin: 0 auto;
  margin-top: 4rem;
}

.header-text {
  text-align: center;
  margin-bottom: 1.5rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid var(--color-border);
}

.title {
  font-size: 2.5rem;
  font-weight: 800;
  color: var(--color-title);
  animation: slideInFromTop 0.5s ease-out;
  letter-spacing: -0.05em;
  text-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
}

.subtitle {
  color: var(--color-text-muted);
  margin-top: 0.5rem;
  font-size: 1rem;
}

@media (min-width: 640px) {
  .title {
    font-size: 3rem;
  }
}

.conversation-area {
  flex-grow: 1;
  overflow-y: auto;
  padding: 1rem;
  background-color: var(--color-dark-background);
  border-radius: 0.75rem;
  box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.2);
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.conversation-area::-webkit-scrollbar {
  width: 8px;
}
.conversation-area::-webkit-scrollbar-thumb {
  background-color: var(--color-primary);
  border-radius: 4px;
  border: 2px solid var(--color-dark-background);
}
.conversation-area::-webkit-scrollbar-track {
  background-color: var(--color-card-background);
}

.message-wrapper {
  display: flex;
  opacity: 0;
  transform: translateY(10px);
  animation: fadeIn 0.5s forwards;
  animation-delay: var(--animation-delay);
}

.message-user {
  justify-content: flex-end;
}

.message-bot {
  justify-content: flex-start;
}

.message-bubble {
  padding: 0.75rem 1rem;
  border-radius: 1rem;
  max-width: 75%;
  word-wrap: break-word;
  transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
}

.bubble-user {
  background-color: var(--color-user-bubble);
  color: var(--color-text-white);
  border-bottom-right-radius: 0.25rem;
}

.bubble-bot {
  background-color: var(--color-bot-bubble);
  color: var(--color-text-white);
  border-bottom-left-radius: 0.25rem;
}

.input-area {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-top: 1rem;
}

.text-input {
  flex-grow: 1;
  padding: 0.5rem 1rem;
  font-size: 1rem;
  border-radius: 9999px;
  background-color: var(--color-card-background);
  color: var(--color-text-white);
  border: 1px solid var(--color-border);
  outline: none;
  transition: all 0.3s ease;
  box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.2);
}

.text-input::placeholder {
  color: var(--color-text-muted);
}

.text-input:focus {
  background-color: #242b38;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.25), inset 0 1px 3px rgba(0, 0, 0, 0.2);
}

.text-input:disabled {
  background-color: #4b5563;
  cursor: not-allowed;
  opacity: 0.8;
}

.send-button {
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 9999px;
  background: linear-gradient(45deg, var(--color-send-button-gradient-start), var(--color-send-button-gradient-end));
  transition: transform 0.3s ease, box-shadow 0.3s ease, background 0.3s ease;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
}

.send-button:hover:not(:disabled) {
  transform: scale(1.05);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.4);
}

.send-button:disabled {
  background: var(--color-border);
  cursor: not-allowed;
  opacity: 0.7;
  box-shadow: none;
}

.send-icon {
  width: 1.25rem;
  height: 1.25rem;
  color: var(--color-text-white);
}

.dot-typing-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 1.25rem;
}

.dot-typing {
  position: relative;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background-color: var(--color-text-muted);
  color: var(--color-text-muted);
  box-shadow: 12px 0 0 -5px, 24px 0 0 -5px;
  animation: dot-typing 1.5s infinite linear;
}

@keyframes dot-typing {
  0% { box-shadow: 12px 0 0 -5px, 24px 0 0 -5px; }
  33.33% { box-shadow: 12px 0 0 0, 24px 0 0 -5px; }
  66.67% { box-shadow: 12px 0 0 0, 24px 0 0 0; }
  100% { box-shadow: 12px 0 0 0, 24px 0 0 0; }
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes slideInFromTop {
  from { transform: translateY(-20px); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}
</style>

