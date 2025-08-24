<template>
  <footer class="global-footer fixed bottom-0 left-0 right-0 z-10 text-center bg-gray-800 text-white">
    <nav class="flex flex-wrap justify-center mx-4">
      <a href="/landing" class="text-gray-300 hover:text-white py-1 mx-2">ホーム</a>
      <a href="/features.html" class="text-gray-300 hover:text-white py-1 mx-2">機能紹介</a>
      <a href="/terms.html" class="text-gray-300 hover:text-white py-1 mx-2">利用規約</a>
      <a href="/privacy.html" class="text-gray-300 hover:text-white py-1 mx-2">プライバシーポリシー</a>
      <a href="/contact.html" class="text-gray-300 hover:text-white py-1 mx-2">お問い合わせ</a>
    </nav>
    <p class="text-xs">&copy; 2025 Olympic Golfer. All rights reserved.</p>
  </footer>
</template>

<script setup lang="ts">
// No script logic needed for a simple footer
</script>

<style scoped>
.global-footer {
  /* Tailwind classes handle most of the styling */
  /* fixed bottom-0 left-0 right-0 z-10 text-center py-4 bg-gray-800 text-white */
}
nav a {
  transition: color 0.3s ease;
}
</style>