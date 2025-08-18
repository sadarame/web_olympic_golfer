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
        <!-- ローディング表示 -->
        <div v-if="isLoading" class="text-center">
          <p class="text-gray-600">ユーザー情報を読み込み中...</p>
        </div>

        <!-- ユーザー情報表示 -->
        <div v-else class="text-center mb-4">
          <div v-if="!isEditingUserName">
            <p class="text-xl font-semibold text-gray-800">
              ようこそ、{{ displayName }}さん！
            </p>
            <button @click="editUserName" class="text-blue-500 hover:underline text-sm mt-1">
              ユーザー名を変更
            </button>
          </div>
          <div v-else>
            <input 
              type="text" 
              v-model="userName" 
              placeholder="カスタムユーザー名を入力"
              class="input-field text-center text-xl font-semibold text-gray-800 w-full" 
            />
            <p v-if="errorMessage" class="text-red-500 text-sm mt-1">{{ errorMessage }}</p>
            <button @click="saveUserName" class="btn-primary mt-2" :disabled="isSaving">
              {{ isSaving ? '保存中...' : '保存' }}
            </button>
            <button @click="cancelEdit" class="btn-secondary mt-2 ml-2">キャンセル</button>
          </div>
        </div>

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
  import { onMounted, watch, nextTick, ref, computed } from 'vue';
  import { useAuthStore } from '../stores/auth';
  import { useRouter } from 'vue-router';
  import { apiService } from '../services/api';
  import type { User, UserRegistrationData } from '../types';

  const authStore = useAuthStore();
  const router = useRouter();

  // ユーザー名編集用のリアクティブ変数
  const userName = ref('');
  const isEditingUserName = ref(false);
  const errorMessage = ref('');
  const isLoading = ref(false);
  const isSaving = ref(false);
  const currentUser = ref<User | null>(null);

  // 表示名を計算（カスタム名があればそれを使用、なければGoogleアカウント名）
  const displayName = computed(() => {
    console.log('currentUser.value', currentUser.value);
    console.log('currentUser.value', currentUser.value?.customName);
    if (currentUser.value?.customName) {
      return currentUser.value.customName;
    }
    return authStore.user?.name || 'ゲスト';
  });

  // JWTデコード関数
  function decodeJwtResponse(token: string) {
    var base64Url = token.split('.')[1];
    var base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    var jsonPayload = decodeURIComponent(atob(base64).split('').map(function(c) {
      return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
    }).join(''));
    return JSON.parse(jsonPayload);
  }

  // ユーザー情報を取得または作成
  const fetchOrCreateUser = async () => {
    if (!authStore.user?.sub || !authStore.token) return;

    isLoading.value = true;
    try {
      // ユーザー情報取得APIを呼び出す
      const existingUser = await apiService.getUser(authStore.token);

      // GPTによる修正
      const user = normalizeUser(existingUser);
      if (user) {
        currentUser.value = user;
        userName.value = user.customName || authStore.user.name || '';
        return;
      }
      throw new Error('User not found');

    } catch (error) {
      console.log('ユーザーが見つからないため、新規作成します:', error);
      
      // ユーザーが存在しない場合は新規作成
      try {
        const userData = {
          userInfo: {
            name: authStore.user.name,
            email: authStore.user.email,
            profile: authStore.user
          },
          customName: authStore.user.name
        };
        
        // ユーザー登録APIを呼び出す
        const newUser = await apiService.registerUser(userData, authStore.token);
        // 画面表示変数に値を設定
        currentUser.value = newUser;
        userName.value = newUser.customName || authStore.user.name || '';

      } catch (createError) {
        console.error('ユーザー作成に失敗しました:', createError);
        errorMessage.value = 'ユーザー情報の作成に失敗しました。';
      }
    } finally {
      isLoading.value = false;
    }
  };

  // コールバック関数
  const handleCredentialResponse = async (response: any) => {

    // デコードしてユーザー情報を取得
    const decoded = decodeJwtResponse(response.credential);
    authStore.setAuthInfo(decoded, response.credential);
    // ログイン後にユーザー情報を取得または作成
    await fetchOrCreateUser();
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

  // authStore.user の変更を監視し、ユーザー情報を取得
  watch(() => authStore.user, (newUser) => {
    if (newUser && authStore.isAuthenticated) {
      fetchOrCreateUser();
    }
  }, { immediate: true });

  // ユーザー名編集モードに入る
  const editUserName = () => {
    isEditingUserName.value = true;
    userName.value = currentUser.value?.customName || authStore.user?.name || '';
    errorMessage.value = '';
  };

  // ユーザー名編集をキャンセル
  const cancelEdit = () => {
    isEditingUserName.value = false;
    userName.value = currentUser.value?.customName || authStore.user?.name || '';
    errorMessage.value = '';
  };

  // ユーザー名を保存する
  const saveUserName = async () => {
    if (!authStore.user?.sub || !authStore.token) return;

    const trimmedUserName = userName.value.trim();
    if (!trimmedUserName) {
      errorMessage.value = 'ユーザー名を入力してください。';
      return;
    }

    isSaving.value = true;
    try {
      const userData = {
        token: authStore.token,
        userInfo: {
          name: authStore.user.name,
          email: authStore.user.email,
          profile: authStore.user
        },
        customName: trimmedUserName
      };

      const updatedUser = await apiService.registerUser(userData, authStore.token);

      // GPTによる修正
      const user = normalizeUser(updatedUser);
      if (!user) throw new Error('ユーザー更新レスポンス不正');
      currentUser.value = user;

      // currentUser.value = updatedUser;
      isEditingUserName.value = false;
      errorMessage.value = '';

    } catch (error) {
      console.error('ユーザー名の更新に失敗しました:', error);
      errorMessage.value = 'ユーザー名の更新に失敗しました。';
    } finally {
      isSaving.value = false;
    }
  };

  const handleStartGame = () => {
    router.push('/start');
  };

  const handleEditFriends = () => {
    alert('友達編集画面への遷移をシミュレートします。');
  };

  const handleViewScores = () => {
    alert('過去のスコア一覧画面への遷移をシミュレートします。');
  };

  // ユーザー情報を正規化する関数
  function normalizeUser(res: any): User | null {
    if (!res) return null;
    const u = 'user' in res ? res.user : res;
    if (!u) return null;
    return {
      uid: u.uid ?? u.userId ?? '',
      email: u.email ?? u.userInfo?.email ?? '',
      name: u.name ?? u.userInfo?.name,
      customName: u.customName,
      createdAt: u.createdAt,
      updatedAt: u.updatedAt,
    } as User;
  }
</script>

<style scoped>
  .btn-google {
    @apply bg-blue-500 text-white hover:bg-blue-600 focus:ring-blue-400;
  }

  .message-box {
    @apply p-4 rounded-lg text-center font-semibold text-white mb-4;
    background-color: #4CAF50; /* 緑色の背景 */
  }

  .input-field {
    @apply border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent;
  }

  .btn-primary {
    @apply bg-green-500 text-white px-4 py-2 rounded-md hover:bg-green-600 transition-colors duration-200;
  }

  .btn-secondary {
    @apply bg-gray-300 text-gray-800 px-4 py-2 rounded-md hover:bg-gray-400 transition-colors duration-200;
  }
</style>