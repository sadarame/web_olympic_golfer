<script setup lang="ts">
</script>

<template>
    <header class="header fixed top-0 left-0 right-0 z-10">
      <h1 class="text-2xl font-bold text-gray-800">
          Golf Olympic ⛳️
      </h1>
      <!-- ログイン状態表示部分 (初期状態では非表示) -->
      <div id="user-info" class="flex items-center space-x-4 hidden">
          <div class="flex items-center space-x-2">
              <img id="user-avatar" src="https://placehold.co/40x40/cccccc/333333?text=User" alt="User Avatar" class="w-10 h-10 rounded-full border-2 border-green-500">
              <span id="user-name" class="font-semibold text-gray-700">ゲストユーザー</span>
          </div>
          <button id="logout-button" class="text-gray-500 hover:text-red-500 transition-colors duration-200">
              ログアウト
          </button>
      </div>
  </header>
  <router-view />
</template>

<style scoped>
  .header {
      background-color: rgba(255, 255, 255, 0.9);
      backdrop-filter: blur(10px);
      -webkit-backdrop-filter: blur(10px);
      box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
      padding: 1rem 2rem;
      display: flex;
      justify-content: space-between; /* 左右に要素を配置 */
      align-items: center;
  }
</style>
