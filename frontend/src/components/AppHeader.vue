<template>
  <header class="bg-green-700 text-white p-4 shadow-md">
    <nav class="container mx-auto flex justify-between items-center">
      <router-link to="/" class="text-2xl font-bold">Golf Olympic ⛳️</router-link>
      <div>
        <!-- Future navigation links can go here -->
      </div>
    </nav>
  </header>
</template>

<script setup lang="ts">
// No specific script logic needed for this simple header yet
</script>

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
