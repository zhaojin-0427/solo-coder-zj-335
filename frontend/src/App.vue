<template>
  <el-container class="layout-container">
    <el-aside width="240px" class="sidebar">
      <div class="logo">
        <el-icon :size="32" color="#fff"><Headset /></el-icon>
        <span class="logo-text">助听器协同平台</span>
      </div>
      <el-menu
        :default-active="activeMenu"
        router
        background-color="#1f2d3d"
        text-color="#c0c4cc"
        active-text-color="#409eff"
        class="menu"
      >
        <el-menu-item index="/profiles">
          <el-icon><User /></el-icon>
          <span>佩戴档案</span>
        </el-menu-item>
        <el-menu-item index="/feedback">
          <el-icon><ChatDotRound /></el-icon>
          <span>场景反馈</span>
        </el-menu-item>
        <el-menu-item index="/adjustments">
          <el-icon><Setting /></el-icon>
          <span>调试记录</span>
        </el-menu-item>
        <el-menu-item index="/followups">
          <el-icon><Calendar /></el-icon>
          <span>复诊跟踪</span>
        </el-menu-item>
        <el-menu-item index="/statistics">
          <el-icon><DataAnalysis /></el-icon>
          <span>统计分析</span>
        </el-menu-item>
      </el-menu>
    </el-aside>
    <el-container>
      <el-header class="header">
        <div class="header-left">
          <el-breadcrumb separator="/">
            <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
            <el-breadcrumb-item v-for="item in breadcrumbs" :key="item.path">
              {{ item.label }}
            </el-breadcrumb-item>
          </el-breadcrumb>
        </div>
        <div class="header-right">
          <el-tag type="success" effect="dark">
            <el-icon :size="12" style="margin-right: 4px"><Connection /></el-icon>
            服务正常
          </el-tag>
        </div>
      </el-header>
      <el-main class="main">
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()

const activeMenu = computed(() => route.path)

const breadcrumbs = computed(() => {
  const map: Record<string, string> = {
    '/profiles': '佩戴档案',
    '/feedback': '场景反馈',
    '/adjustments': '调试记录',
    '/followups': '复诊跟踪',
    '/statistics': '统计分析'
  }
  const result: { path: string; label: string }[] = []
  let current = ''
  for (const seg of route.path.split('/').filter(Boolean)) {
    current += '/' + seg
    if (map[current]) {
      result.push({ path: current, label: map[current] })
    } else if (!isNaN(Number(seg))) {
      result.push({ path: current, label: '详情' })
    }
  }
  return result
})
</script>

<style scoped>
.layout-container {
  height: 100vh;
}

.sidebar {
  background: #1f2d3d;
  overflow-y: auto;
}

.logo {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 24px 20px;
  background: #18222e;
  border-bottom: 1px solid #2d3a4b;
}

.logo-text {
  color: #fff;
  font-size: 16px;
  font-weight: 600;
}

.menu {
  border-right: none;
}

.header {
  background: #fff;
  border-bottom: 1px solid #e4e7ed;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
}

.header-left {
  flex: 1;
}

.main {
  background: #f5f7fa;
  overflow-y: auto;
  padding: 24px;
}
</style>
