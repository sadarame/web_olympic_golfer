<template>
    <!-- ヘッダー部分 -->
    <header class="header fixed top-0 left-0 right-0 z-10 flex items-center justify-between">
        <h1 class="text-2xl font-bold text-gray-800">
            Golf Olympic ⛳️
        </h1>
        <!-- ログイン状態表示部分 -->
        <div id="user-info" class="flex items-center space-x-4 relative">
            <div id="user-profile-button" class="flex items-center space-x-2 cursor-pointer p-2 rounded-full hover:bg-gray-100 transition-colors duration-200">
                <img id="user-avatar" :src="authStore.user?.picture || 'https://placehold.co/40x40/cccccc/333333?text=User'" alt="User Avatar" class="w-10 h-10 rounded-full border-2 border-green-500">
                
            </div>
            <!-- ホバーメニュー (初期状態では非表示) -->
            <div id="hover-menu" class="absolute right-0 top-14 mt-2 w-48 bg-white rounded-md shadow-lg py-1 hidden z-20" v-if="authStore.isAuthenticated">
                <button id="logout-button" @click="handleLogout" class="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">
                    ログアウト
                </button>
            </div>
        </div>
    </header>
</template>

<script setup lang="ts">
import { useAuthStore } from '../stores/auth';

const authStore = useAuthStore();

const handleLogout = () => {
  authStore.clearAuthInfo();
  alert('ログアウトしました。');
  // Optionally, redirect to login page or home page
};
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
