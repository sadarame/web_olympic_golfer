<template>
    <!-- ヘッダー部分 -->
    <header class="header fixed top-0 left-0 right-0 z-10 flex items-center justify-between">
        <h1 class="text-2xl font-bold text-gray-800 cursor-pointer" @click="goToHome">
            Golf Olympic  <span class="inline-block golf-ball-bounce">⛳️</span>
        </h1>
        <!-- ログイン状態表示部分 -->
        <div id="user-info" class="flex items-center space-x-4 relative group">
            <div id="user-profile-button" class="flex items-center space-x-2 cursor-pointer p-2 rounded-full hover:bg-gray-100 transition-colors duration-200">
                <img
                    id="user-avatar"
                    :src="authStore.user?.photoURL || 'https://placehold.co/40x40/cccccc/333333?text=None'"
                    alt="User Avatar"
                    class="w-10 h-10 rounded-full border-2"
                    :class="{
                        'border-green-500': authStore.user?.photoURL,
                        'border-gray-500': !authStore.user?.photoURL
                    }"
                />
            </div>
            <!-- ホバーメニュー (初期状態では非表示) -->
            <div id="hover-menu" class="absolute right-0 top-14 mt-2 w-48 bg-white rounded-md shadow-lg py-1 hidden z-20 group-hover:block" v-if="authStore.isAuthenticated">
                <button id="logout-button" @click="handleLogout" class="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">
                    ログアウト
                </button>
            </div>
        </div>
    </header>
</template>

<script setup lang="ts">
    import { useAuthStore } from '../stores/auth';
    import { useRoundStore } from '../stores/round';
    import { useRouter } from 'vue-router';
    import { signOut } from 'firebase/auth'; // Firebase signOut をインポート
    import { auth } from '../main'; // Firebase auth インスタンスをインポート

    const router = useRouter();
    const authStore = useAuthStore();
    const roundStore = useRoundStore();

    const handleLogout = async () => {
        try {
            await signOut(auth);
            // Firebase の認証状態が変更されると App.vue の onAuthStateChanged が発火し、
            // authStore.clearAuthInfo() が呼び出されるため、ここではストアの更新は不要
            roundStore.clearRouundInfo(); // ラウンド情報はここでクリア
            router.push('/');
        } catch (error) {
            console.error("ログアウトに失敗しました:", error);
        }
    };

    const goToHome = () => {
        roundStore.clearRouundInfo();
        router.push('/');
    };
</script>

<style scoped>
    .header { /* This style block is for the header element itself */
    background-color: rgba(255, 255, 255, 0.9);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    padding: 0.1rem 1rem;
    /* Removed display: flex, justify-content, align-items from here */
    }

    /* 遊び心を追加するアニメーション */
    @keyframes bounce-ball {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-5px); }
    }

    .golf-ball-bounce {
        animation: bounce-ball 0.8s infinite ease-in-out;
    }
</style>
