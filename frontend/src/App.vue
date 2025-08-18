<script setup lang="ts">
    import { onMounted } from 'vue';
    import { onAuthStateChanged } from 'firebase/auth';
    import { auth } from './main';
    import { useAuthStore } from './stores/auth';
    import AppHeader from './components/AppHeader.vue';

    const authStore = useAuthStore();

    onMounted(() => {
      onAuthStateChanged(auth, (user) => {
        // Firebase の認証状態が変更されるたびに Pinia ストアを更新
        authStore.setAuthInfoFromFirebase();
      });
    });
</script>

<template>
  <AppHeader />
  <router-view />
</template>

<style scoped>
</style>
