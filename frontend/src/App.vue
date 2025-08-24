<script setup lang="ts">
    import { onMounted } from 'vue';
    import { onAuthStateChanged } from 'firebase/auth';
    import { auth } from './firebase';
    import { useAuthStore } from './stores/auth';
    import AppHeader from './components/AppHeader.vue';
    import LoadingSpinner from './components/LoadingSpinner.vue'; // Add this import

    const authStore = useAuthStore();

    onMounted(() => {
      onAuthStateChanged(auth, () => {
        // Firebase の認証状態が変更されるたびに Pinia ストアを更新
        authStore.setAuthInfoFromFirebase();
      });
    });
</script>

<template>
  <AppHeader />
  <router-view />
  <LoadingSpinner /> <!-- Add this line -->
</template>

<style scoped>
</style>
