<template>
  <div class="game-view">
    <Header />
    <div class="game-content">
      <h1>游戏页面</h1>
      <div class="chatbox">
      <div class="messages">
        <div v-for="(message, index) in messages" :key="index" :class="message.sender">
          {{ message.text }}
        </div>
      </div>
      <input v-model="inputMessage" @keyup.enter="sendMessage" placeholder="输入消息..." />
    </div>
      <router-link to="/" class="back-button">返回首页</router-link>
    </div>
  </div>
</template>

<script setup>
import Header from '@/components/Header.vue'
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios';

const messages = ref([]);
const inputMessage = ref('');

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
  min-height: calc(100vh - 60px);
}

.game-content {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
  text-align: center;
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
  width: 300px;
  margin-left: auto;
  margin-right: auto;
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