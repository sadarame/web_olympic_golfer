<template>
  <div class="main-layout pt-16">
    <div class="container mx-auto p-4 md:p-8 max-w-sm card">
    <!-- ページタイトル -->
      <div class="text-4xl font-bold text-center mb-2 text-gray-800">
        ⛳️
      </div>
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
            data-client_id="735464206154-01ti9otrmjqaqukdlo2956bejgu33u14.apps.googleusercontent.com"
            data-callback="handleCredentialResponse"
            data-auto_prompt="false">
        </div>
        <div class="g_id_signin inline-block"
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
              placeholder="ユーザー名を変更"
              class="input-field text-center text-xl font-semibold text-gray-800 w-full" 
            />
            <p v-if="errorMessage" class="text-red-500 text-sm mt-1">{{ errorMessage }}</p>
            <button @click="saveUserName" class="btn-primary mt-2" :disabled="isSaving">
              {{ isSaving ? '保存中...' : '保存' }}
            </button>
            <button @click="cancelEdit" class="btn-secondary mt-2 ml-2">キャンセル</button>
          </div>
        </div>

        <button @click="handleStartGame" class="btn-solid">
          ゲームを始める 🏌️‍♂️
        </button>
        <button @click="handleEditFriends" class="btn-solid">
          友達編集 🤝
        </button>
        <button @click="handleViewScores" class="btn-solid">
          過去のスコア一覧 📊
        </button>
        <button @click="handleReview" class="btn-solid">
          レビュー ⭐️
        </button>
      </div>
    </div>
  </div>
  <GlobalFooter />
</template>

<script setup lang="ts">
  import { onMounted, watch, nextTick, ref, computed } from 'vue';
  import { useAuthStore } from '../stores/auth';
  import { useRouter } from 'vue-router';
  import { apiService } from '../services/api';
  import type { User } from '../types';
  import { GoogleAuthProvider, signInWithCredential } from 'firebase/auth'; // Firebase Auth をインポート
  import { auth } from '../firebase'; // Firebase auth インスタンスをインポート
  import { useRoundStore } from '../stores/round'; // 追加: roundStoreのインポート
  import GlobalFooter from '../components/GlobalFooter.vue'; // GlobalFooter コンポーネントをインポート

  const authStore = useAuthStore();
  const router = useRouter();
  const roundStore = useRoundStore(); // 追加: roundStoreの初期化
  // インプットフィールドとして使用
  const userName = ref('');
  const isEditingUserName = ref(false);
  const errorMessage = ref('');
  const isLoading = ref(false);
  const isSaving = ref(false);

  // 表示名を計算（カスタム名があればそれを使用、なければGoogleアカウント名）
  const displayName = computed(() => {
    const name = authStore.user?.customName || 'ゲスト';
    return name;
  });

  // ユーザー情報を取得または作成
  // ログイン時のみ呼ばれるコールバック後に実行
  const fetchOrCreateUser = async () => {
    // 認証済みだったらFeatchはしない
    if (!auth.currentUser) return;

    isLoading.value = true;

    try {
      // ユーザー情報取得APIを呼び出す
      const existingUser = await apiService.getUser(); // トークンはapiService内で取得される

      // GPTによる修正
      const user = normalizeUser(existingUser);

      if (user) {
        // ストアのユーザー名を更新
        authStore.updateCustomName(user.customName ?? '');
        return;
      }
      throw new Error('User not found');

    } catch (error) {
      console.log('ユーザーが見つからないため、新規作成します:', error);
      
      // ユーザーが存在しない場合は新規作成
      try {
        const userData = {
          userInfo: {
            name: auth.currentUser.displayName || '',
            email: auth.currentUser.email || '',
            profile: auth.currentUser.toJSON() // Firebase User オブジェクトをJSONとして保存
          },
          customName: auth.currentUser.displayName || '',
        };
        
        // ユーザー登録APIを呼び出す
        await apiService.registerUser(userData); // トークンはapiService内で取得される

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
    // Google IDトークンをFirebaseの認証情報に変換
    const credential = GoogleAuthProvider.credential(response.credential);

    try {
      // Firebase にサインイン
      await signInWithCredential(auth, credential);
      // Firebase の認証状態が変更されると App.vue の onAuthStateChanged が発火し、
      // authStore.setAuthInfoFromFirebase() が呼び出されるため、ここではストアの更新は不要

      // ログイン後にユーザー情報を取得または作成
      await fetchOrCreateUser();
    } catch (error) {
      console.error("Firebase sign-in with Google credential failed:", error);
      errorMessage.value = 'ログインに失敗しました。';
    }
  };

  const renderGoogleButton = () => {
    const googleAccounts = (window as any).google?.accounts?.id;
    const signInButton = document.querySelector(".g_id_signin") as HTMLElement;

    if (googleAccounts && signInButton) {
      googleAccounts.initialize({
        client_id: "735464206154-01ti9otrmjqaqukdlo2956bejgu33u14.apps.googleusercontent.com",
        callback: handleCredentialResponse,
      });
      googleAccounts.renderButton(
        signInButton,
        { type: "standard", size: "large", theme: "outline", text: "sign_in_with", shape: "rectangular", logo_alignment: "left" }
      );
    }
  };

  // ユーザー名編集モードに入る
  const editUserName = () => {
    isEditingUserName.value = true;
    // 編集モード時に今のカスタムネームをインプットフィールドに設定する
    userName.value = authStore.user?.customName || '';
    errorMessage.value = '';
  };

  // ユーザー名編集をキャンセル
  const cancelEdit = () => {
    isEditingUserName.value = false;
    errorMessage.value = '';
  };

  // ユーザー名を保存する
  const saveUserName = async () => {
    if (!auth.currentUser) return; // Firebase ユーザーが認証されていることを確認
    // トリムして変数に設定
    const trimmedUserName = userName.value.trim();
      
    if (!trimmedUserName) {
        errorMessage.value = 'ユーザー名を入力してください。';
        return;
    }
    isSaving.value = true;
    try {
      const userData = {
        userInfo: {
          name: auth.currentUser.displayName || '',
          email: auth.currentUser.email || '',
          profile: auth.currentUser.toJSON() // Firebase User オブジェクトをJSONとして保存
        },
        customName: trimmedUserName
      };

      // API呼び出し
      const updatedUser = await apiService.registerUser(userData); // トークンはapiService内で取得される

      // 正規化してユーザー情報を更新
      const user = normalizeUser(updatedUser);
      if (!user) throw new Error('ユーザー更新レスポンス不正');

      // ストアのユーザー名を更新
      authStore.updateCustomName(user.customName ?? '');

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
    router.push('/friends');
  };

  const handleViewScores = () => {
    router.push('/past-games');
  };

  const handleReview = () => {
    router.push('/review');
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


  // 認証状態の変化を監視し、Googleボタンをレンダリング（headerのログアウト対策）
  watch(() => authStore.isAuthenticated, (newIsAuthenticated) => {
    if (!newIsAuthenticated) {
      nextTick(() => {
        renderGoogleButton();
      });
    }
  }, { immediate: true });

  onMounted(() => {
    (window as any).handleCredentialResponse = handleCredentialResponse;
    fetchOrCreateUser();
    roundStore.clearRouundInfo();
  });

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