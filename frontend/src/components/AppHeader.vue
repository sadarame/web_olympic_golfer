<template>
  <header class="bg-green-700 text-white p-4 shadow-md"> <!-- Removed fixed positioning classes -->
    <div class="container mx-auto flex flex-col items-center"> <!-- Changed to flex-col and items-center -->
      <!-- Site Title -->
      <h1 class="text-2xl font-bold text-white">Golf Olympic ⛳️</h1> <!-- Changed text color to white -->
      <!-- Login Status Display Part -->
      <div id="user-info" class="flex items-center space-x-4 mt-2"> <!-- Added mt-2 for spacing -->
          <div class="flex items-center space-x-2">
              <img id="user-avatar" src="https://placehold.co/40x40/cccccc/333333?text=User" alt="User Avatar" class="w-10 h-10 rounded-full border-2 border-green-500">
              <span id="user-name" class="font-semibold text-white">ゲストユーザー</span> <!-- Changed text color to white -->
          </div>
          <button id="logout-button" class="text-white hover:text-red-200 transition-colors duration-200"> <!-- Changed text color to white -->
              ログアウト
          </button>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
// No specific script logic needed for this simple header yet
</script>

<style scoped>
.header { /* This style block is for the header element itself */
  background-color: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  padding: 1rem 2rem;
  /* Removed display: flex, justify-content, align-items from here */
}
</style>
