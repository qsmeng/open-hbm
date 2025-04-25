<!-- /f:/workspace/open-hbm/src/components/Header.vue -->
<template>
  <header class="app-header">
    <div class="left-section">
      <router-link to="/">首页</router-link>
      <router-link to="/explore">探索</router-link>
      <router-link to="/rules">规则</router-link>
    </div>
    <div class="right-section">
      <router-link v-if="!isLoggedIn" to="/auth">登录/注册</router-link>
      <div v-else class="user-info">
        <span>{{ username }}</span>
        <button @click="logout">退出</button>
      </div>
    </div>
  </header>
</template>

<script>
export default {
  data() {
    return {
      isLoggedIn: false, // This should be managed according to your auth system
      username: '' // This should be populated with actual user data
    }
  },
  methods: {
    logout() {
      // Implement logout logic here
    }
  }
}
</script>

<style scoped>
.app-header {
  display: flex;
  justify-content: space-between;
  padding: 1rem;
  background-color: #f5f5f5;
}

.left-section, .right-section {
  display: flex;
  gap: 1rem;
}

/* You can add more styles as needed */
</style>
