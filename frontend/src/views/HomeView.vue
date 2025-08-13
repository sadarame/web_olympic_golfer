<template>
  <div class="main-layout">
    <div class="container mx-auto p-4 md:p-8 max-w-sm card">
    <!-- ページタイトル -->
      <h1 class="text-4xl font-bold text-center mb-4 text-gray-800">
        ⛳️
      </h1>
      <p class="text-center text-gray-600 mb-8">
        オリンピックゴルフの<br>
        スコアを楽しく記録しよう！😊
      </p>

      <!-- アプリ説明 -->
      <p class="text-center text-gray-700 mb-8 leading-relaxed">
        
        <div v-if="!authStore.isAuthenticated">
          Googleアカウントでの<br>
          ログインが必要です
        </div>
      </p>

      <!-- ログインセクション -->
      <div v-if="!authStore.isAuthenticated" class="text-center">
        <!-- Google Sign-In button -->
        <div id="g_id_onload"
            data-client_id="662503012810-fh86an6fbiu8bm34mrh4kuu98u3c3i1q.apps.googleusercontent.com"
            data-callback="handleCredentialResponse"
            data-auto_prompt="false">
        </div>
        <div class="g_id_signin"
            data-type="standard"
            data-size="large"
            data-theme="outline"
            data-text="sign_in_with"
            data-shape="rectangular"
            data-logo_alignment="left">
        </div>
      </div>

      <!-- ログイン後の表示 -->
      <div v-else class="flex flex-col space-y-4">
        <button @click="handleStartGame" class="w-full group relative inline-flex h-12 items-center justify-center overflow-hidden rounded-md border border-neutral-200 bg-transparent px-6 font-medium text-neutral-600 transition-all duration-100 [box-shadow:3px_3px_rgb(60_80_60)] active:translate-x-[2px] active:translate-y-[2px] active:[box-shadow:0px_0px_rgb(60_80_60)]">
          ゲームを始める 🏌️‍♂️
        </button>
        <button @click="handleEditFriends" class="w-full group relative inline-flex h-12 items-center justify-center overflow-hidden rounded-md border border-neutral-200 bg-transparent px-6 font-medium text-neutral-600 transition-all duration-100 [box-shadow:3px_3px_rgb(60_80_60)] active:translate-x-[2px] active:translate-y-[2px] active:[box-shadow:0px_0px_rgb(60_80_60)]">
          友達編集 🤝
        </button>
        <button @click="handleViewScores" class="w-full group relative inline-flex h-12 items-center justify-center overflow-hidden rounded-md border border-neutral-200 bg-transparent px-6 font-medium text-neutral-600 transition-all duration-100 [box-shadow:3px_3px_rgb(60_80_60)] active:translate-x-[2px] active:translate-y-[2px] active:[box-shadow:0px_0px_rgb(60_80_60)]">
          過去のスコア一覧 📊
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
  import { onMounted, watch, nextTick } from 'vue';
  import { useAuthStore } from '../stores/auth';
  import { useRouter } from 'vue-router';

  const authStore = useAuthStore();
  const router = useRouter();

  // JWTデコード関数
  function decodeJwtResponse(token: string) {
    var base64Url = token.split('.')[1];
    var base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    var jsonPayload = decodeURIComponent(atob(base64).split('').map(function(c) {
      return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
    }).join(''));
    return JSON.parse(jsonPayload);
  }

  // コールバック関数
  const handleCredentialResponse = (response: any) => {
    console.log("Encoded JWT ID token: " + response.credential);
    const decoded = decodeJwtResponse(response.credential);
    console.log("Decoded JWT payload:", decoded);

    authStore.setAuthInfo(decoded, response.credential); // Save user info and token to Pinia store
    alert('Googleログイン成功！IDトークンをコンソールで確認してください。');
  };

  const renderGoogleButton = () => {
    const googleAccounts = (window as any).google?.accounts?.id;
    const signInButton = document.querySelector(".g_id_signin") as HTMLElement;

    if (googleAccounts && signInButton) {
      googleAccounts.initialize({
        client_id: "662503012810-fh86an6fbiu8bm34mrh4kuu98u3c3i1q.apps.googleusercontent.com",
        callback: handleCredentialResponse,
      });
      googleAccounts.renderButton(
        signInButton,
        { type: "standard", size: "large", theme: "outline", text: "sign_in_with", shape: "rectangular", logo_alignment: "left" }
      );
    }
  };

  onMounted(() => {
    (window as any).handleCredentialResponse = handleCredentialResponse;
  });

  watch(() => authStore.isAuthenticated, (newIsAuthenticated) => {
    if (!newIsAuthenticated) {
      nextTick(() => {
        renderGoogleButton();
      });
    }
  }, { immediate: true });

  const handleStartGame = () => {
    router.push('/start');
  };

  const handleEditFriends = () => {
    alert('友達編集画面への遷移をシミュレートします。');
  };

  const handleViewScores = () => {
    alert('過去のスコア一覧画面への遷移をシミュレートします。');
  };
</script>

<style scoped>
  .btn-google {
    @apply bg-blue-500 text-white hover:bg-blue-600 focus:ring-blue-400;
  }

  .message-box {
    @apply p-4 rounded-lg text-center font-semibold text-white mb-4;
    background-color: #4CAF50; /* 緑色の背景 */
  }
</style>