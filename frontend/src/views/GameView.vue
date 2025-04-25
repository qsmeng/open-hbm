<template>
  <div class="game-view">
    <Header />
    <div class="game-container">
      <!-- Main game area -->
      <div class="game-main">
        <h1>游戏页面</h1>
        <div class="chatbox">
          <div class="messages">
            <div v-for="(message, index) in messages" :key="index" :class="message.sender">
              {{ message.text }}
            </div>
          </div>
          <input v-model="inputMessage" @keyup.enter="sendMessage" placeholder="输入消息..." />
        </div>
      </div>
      
      <!-- AI responses section -->
      <div class="ai-responses">
        <h3>AI备选回复</h3>
        <div class="response-options">
          <!-- AI generated responses will appear here -->
        </div>
      </div>
      
      <!-- Treasure image section -->
      <div class="treasure-area">
        <img :src="treasureImage" alt="宝物" @error="setDefaultImage">
      </div>
    </div>
    <router-link to="/" class="back-button">返回首页</router-link>
    <Footer />
  </div>
</template>

<script setup>
import Header from '@/components/Header.vue'
import Footer from '@/components/Footer.vue'
import { ref } from 'vue'
import axios from 'axios'

const messages = ref([])
const inputMessage = ref('')
const treasureImage = ref('background.png')

const setDefaultImage = (e) => {
  e.target.src = 'background.png'
}

const sendMessage = async () => {
  if (inputMessage.value.trim() === '') return;

  // 添加用户消息
  messages.value.push({ sender: 'user', text: inputMessage.value });

  // 调用后台接口
  try {
    const response = await axios.post('/api/ollamaByLangchain', { message: inputMessage.value });
    messages.value.push({ sender: 'bot', text: response.data.response });
  } catch (error) {
    console.error('Error sending message:', error);
    messages.value.push({ sender: 'bot', text: '抱歉，暂时无法处理您的请求。' });
  }

  // 清空输入框
  inputMessage.value = '';
};
</script>

<style scoped>
.game-view {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.game-container {
  display: flex;
  flex: 1;
  padding: 20px;
  gap: 20px;
}

.game-main {
  flex: 2;
}

.ai-responses {
  flex: 1;
  border: 1px solid #ddd;
  padding: 10px;
  border-radius: 5px;
}

.treasure-area {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
}

.treasure-area img {
  max-width: 100%;
  max-height: 300px;
  object-fit: contain;
}

.ai-options {
  width: 30%;
  padding: 1rem;
  border-right: 1px solid #ccc;
  overflow-y: auto;
}

.treasure-display {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
}

.treasure-display img {
  max-width: 100%;
  max-height: 300px;
  object-fit: contain;
}

.back-button {
  display: inline-block;
  margin-top: 20px;
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  text-decoration: none;
  border-radius: 5px;
  position: fixed;
  bottom: 20px;
  right: 20px;
}

.back-button:hover {
  background-color: #0056b3;
}

.chatbox {
  height: calc(100vh - 160px);
  margin-top: 20px;
  width: 100%;
  border: 1px solid #ccc;
  border-radius: 5px;
  padding: 10px;
  overflow: auto;
}

.messages {
  height: 200px;
  overflow-y: auto;
  margin-bottom: 10px;
}

.user {
  text-align: right;
  color: #007bff;
}

.bot {
  text-align: left;
  color: #333;
}

input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
}
</style>