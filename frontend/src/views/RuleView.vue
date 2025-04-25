<template>
  <div class="rule-view">
    <Header />
    <div class="rule-content">
      <h1>游戏规则</h1>
      <router-link to="/" class="back-button">返回首页</router-link>
      <section>
      <h2>世界背景</h2>
      <p>在一场前所未有的空间波动灾难之后，我们的世界被分裂成两部分：表世界保留着原本世界的模样；而里世界则由无数碎片化的空间组成。</p>
    </section>
    <section>
      <h2>核心玩法</h2>
      <ul>
        <li>玩家可以通过探索空间获取宝物。</li>
        <li>每个空间都有独特的行动轮次限制。</li>
        <li>团队探索时，AI会根据成员选择生成最终行动。</li>
      </ul>
    </section>
    <section>
      <h2>名词解释</h2>
      <dl>
        <dt>空间</dt>
        <dd>游戏中探索的主要区域，分为个人空间、团队空间和公共空间。</dd>
        <dt>行动轮次</dt>
        <dd>玩家在个人探索中可用的操作次数，初始为1到19次。</dd>
        <dt>宝物</dt>
        <dd>具有独特效果和强度的物品，影响游戏进程。</dd>
        <dt>AI对话系统</dt>
        <dd>允许玩家输入内容，选择或自定义AI生成的多个候选回复之一，实现高度个性化的互动体验。</dd>
      </dl>
    </section>
    </div>
  </div>
</template>

<script setup>
import Header from '@/components/Header.vue'
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
</script>

<style scoped>
.rule-view {
  min-height: calc(100vh - 60px); /* Subtract header height */
}

.rule-content {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
  line-height: 1.6;
}
.rule-content h2 {
  margin-top: 1.5rem;
}
.rule-content ul, .rule-content ol {
  margin-left: 1.5rem;
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
</style>