<template>
  <div class="home-view">
    <Header />
    <main class="main-content">
      <section class="intro">
        <h2 class="section-title">欢迎来到半数黑金</h2>
        <p class="description">
          这是一个以宝物收集与故事探索为核心的创新游戏，利用AI技术推动情节发展，通过社区分享和讨论鼓励玩家共同构建一个丰富多彩的故事世界。
        </p>
        <router-link class="start-button" to="/game">开始探索</router-link>
      </section>

      <section class="features">
        <h2 class="section-title">游戏特色</h2>
        <ul class="feature-list">
          <li class="feature-item">独特的宝物收集系统</li>
          <li class="feature-item">AI驱动的故事生成</li>
          <li class="feature-item">完全自由的个人探索</li>
          <li class="feature-item">多人协作的团队探索</li>
          <li class="feature-item">丰富的公共探索区域</li>
        </ul>
      </section>
    </main>

    <footer class="footer">
      <p>&copy; 2024 半数黑金项目</p>
    </footer>
  </div>
</template>

<script setup>
import Header from '@/components/Header.vue'
import { ref, onMounted } from 'vue'
import { useAuth } from '@/composables/useAuth'

const { isAuthenticated, username, userAvatar } = useAuth()
</script>

<style scoped>
.home-view {
  display: flex;
  flex-direction: column;
  min-height: calc(100vh - 60px);
}

.main-content {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.main {
  flex: 1;
}

.header, .footer {
  text-align: center;
  padding: 20px;
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

.nav-item, .feature-item {
  margin: 0 10px;
  color: #666;
  cursor: pointer;
  text-decoration: none;
}

.nav-item:hover, .feature-item:hover {
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

.main {
  flex: 1;
}

.intro, .features {
  margin-bottom: 30px;
}

.section-title {
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 15px;
}

.description {
  color: #666;
  margin-bottom: 20px;
}

.start-button {
  background-color: #007bff;
  color: #fff;
  padding: 10px 20px;
  border-radius: 5px;
  text-decoration: none;
}

.feature-list {
  list-style: none;
  padding: 0;
}

.feature-item {
  padding: 10px;
  border-bottom: 1px solid #eee;
}
</style>