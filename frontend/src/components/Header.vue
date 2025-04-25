<template>
  <header class="header">
    <h1 class="title">半数黑金</h1>
    <nav class="nav">
      <router-link class="nav-item" to="/">首页</router-link>
      <router-link class="nav-item" to="/game">探索</router-link>
      <router-link class="nav-item" to="/rule">规则</router-link>
      <router-link v-if="isAuthenticated" class="nav-item" to="/user">个人中心</router-link>
      <router-link v-else class="nav-item" to="/auth">登录</router-link>
      <div v-if="isAuthenticated" class="user-info">
        <img :src="userAvatar" class="user-avatar" alt="用户头像">
        <span class="username">{{ username }}</span>
      </div>
    </nav>
  </header>
</template>

<script setup>
import { useAuth } from '@/components/useAuth'

const { isAuthenticated, username, userAvatar } = useAuth()
</script>

<style scoped>
.header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 60px;
  z-index: 1000;
  background: white;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
}

.title {
  font-size: 24px;
  font-weight: bold;
  color: #333;
}

.nav {
  margin-top: 15px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.nav-item {
  margin: 0 10px;
  color: #666;
  cursor: pointer;
  text-decoration: none;
}

.nav-item:hover {
  color: #333;
  text-decoration: underline;
}

.user-info {
  margin-left: 20px;
  display: flex;
  align-items: center;
}

.user-avatar {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  margin-right: 8px;
}

.username {
  font-size: 14px;
  color: #333;
}
</style>