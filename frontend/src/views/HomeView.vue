<template>
  <div class="container mx-auto p-4 md:p-8 max-w-sm card">
    <!-- アプリタイトル -->
    <h1 class="text-4xl font-bold text-center mb-4 text-gray-800">
      Golf Olympic ⛳️
    </h1>
    <p class="text-center text-gray-600 mb-8">
      スコアを楽しく記録しよう！😊
    </p>

    <!-- アプリ説明 -->
    <p class="text-center text-gray-700 mb-8 leading-relaxed">
      ゴルフのオリンピックスコアを記録するツールです✨<br>
      Googleアカウントでのログインが必要です。
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
    <div v-else class="text-center">
      <button @click="handleStartGame" class="btn btn-start">
        ゲームを始める 🏌️‍♂️
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
  import { onMounted } from 'vue'; // Add onMounted
  import { useAuthStore } from '../stores/auth';

  const authStore = useAuthStore();

  function decodeJwtResponse(token: string) {
    var base64Url = token.split('.')[1];
    var base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    var jsonPayload = decodeURIComponent(atob(base64).split('').map(function(c) {
      return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
    }).join(''));
    return JSON.parse(jsonPayload);
  }

  // This function will be called by Google's GIS library
  // It needs to be globally accessible, so we attach it to window
  const handleCredentialResponse = (response: any) => {
    console.log("Encoded JWT ID token: " + response.credential);
    const decoded = decodeJwtResponse(response.credential);
    console.log("Decoded JWT payload:", decoded);

    authStore.setAuthInfo(decoded, response.credential); // Save user info and token to Pinia store
    alert('Googleログイン成功！IDトークンをコンソールで確認してください。');
  };

  onMounted(() => {
    // Attach the function to window after the component is mounted
    (window as any).handleCredentialResponse = handleCredentialResponse;

    const renderGoogleButton = () => {
      const googleAccounts = (window as any).google?.accounts?.id;
      const signInButton = document.querySelector(".g_id_signin") as HTMLElement;

      console.log("renderGoogleButton called.");
      console.log("googleAccounts:", googleAccounts);
      console.log("signInButton:", signInButton);

      if (googleAccounts && signInButton) {
        console.log("Attempting to initialize and render Google button.");
        // Initialize the Google Identity Services client
        googleAccounts.initialize({
          client_id: "662503012810-fh86an6fbiu8bm34mrh4kuu98u3c3i1q.apps.googleusercontent.com",
          callback: (window as any).handleCredentialResponse,
        });

        // Render the button
        googleAccounts.renderButton(
          signInButton,
          { type: "standard", size: "large", theme: "outline", text: "sign_in_with", shape: "rectangular", logo_alignment: "left" } // customization attributes
        );
      } else {
        // If not ready, try again after a short delay
        setTimeout(renderGoogleButton, 100);
      }
    };

    renderGoogleButton(); // Initial call
  });

  const handleStartGame = () => {
    alert('次の画面（開始画面）への遷移をシミュレートします。');
  };
</script>

<style scoped>
  .card {
    background-color: rgba(255, 255, 255, 0.9);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border-radius: 1.5rem; /* より丸みのあるデザインに */
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15); /* 影を強調 */
    padding: 2rem;
    border: 1px solid rgba(255, 255, 255, 0.3);
  }

  .btn {
    @apply w-full py-3 px-6 font-bold rounded-full shadow-lg transition-all duration-300 transform hover:scale-105 active:scale-95 focus:outline-none focus:ring-2 focus:ring-offset-2;
  }

  .btn-google {
    @apply bg-blue-500 text-white hover:bg-blue-600 focus:ring-blue-400;
  }

  .btn-start {
    @apply bg-white text-gray-800 hover:bg-gray-100 focus:ring-gray-300;
  }

  .message-box {
    @apply p-4 rounded-lg text-center font-semibold text-white mb-4;
    background-color: #4CAF50; /* 緑色の背景 */
  }
</style>