<template>
    <div class="main-layout">
        <div class="container mx-auto p-4 md:p-8 max-w-md card">
            <h1 class="text-3xl font-bold text-center text-gray-800 mb-6">
                同伴者を追加👬
            </h1>

            <!-- 新規プレイヤー追加セクション -->
            <div class="space-y-4 mb-8  rounded-lg">
                <h2 class="font-semibold text-gray-800">新しい同伴者を追加✨</h2>
                <div>
                    <!-- プレイヤー名入力欄 -->
                    <input type="text" v-model="newPlayerName" class="input-field w-full h-12" placeholder="同伴者名を入力...">
                    <button @click="addNewPlayer" class="btn-solid w-full h-12 mt-2" type="button">
                        追加
                    </button>
                </div>
                <p v-if="errorMessage" class="text-red-500 text-sm mt-1">{{ errorMessage }}</p>
            </div>

            <!-- 既存プレイヤーリストセクション -->
            <div class="space-y-4 mb-8 bg-gray-50 rounded-lg">
                <h2 class="font-semibold text-gray-800">登録済プレイヤーから選択👥</h2>
                <div>
                    <input
                    v-model="searchQuery"
                    placeholder="名前で検索..."
                    class="input-field w-full h-12"
                    >
                    <div class="text-right mt-1">
                        <button @click="clearSearch" class="btn-secondary">クリア</button>
                    </div>
                </div>
                <div class="space-y-1 h-50 overflow-y-scroll custom-scrollbar p-2 border border-gray-200 rounded-lg">
                    <div v-for="player in filteredPlayers" :key="player.id" @click="toggleSelection(player)"
                        :class="['player-list-item', { 'selected': isSelected(player), 'current-user-highlight': player.id === currentUser.id }]">
                        <div class="flex items-center space-x-3">
                            <input type="checkbox" :checked="isSelected(player)" :disabled="player.id === currentUser.id" class="main-checkbox">
                            <span class="text-gray-800 font-medium">{{ player.name }}</span>
                        </div>
                    </div>
                </div>
            </div>

            <!-- ラウンド参加メンバーリストセクション -->
            <div class="space-y-4 mb-6 rounded-lg">
                <h2 class="font-semibold text-gray-800">ラウンドに参加する同伴者🏌️</h2>
                <div class="space-y-2">
                    <div v-for="player in selectedPlayers" :key="player.id" class="player-list-item">
                        <span class="text-gray-800 font-medium">{{ player.name }}</span>
                        <button v-if="player.id !== currentUser.id" @click="removePlayer(player)" class="btn-danger">
                            ×
                        </button>
                    </div>
                </div>
            </div>
            
            <!-- 次へボタン -->
            <div class="text-center">
                <button @click="startGame" :disabled="selectedPlayers.length < 1" class="btn-solid">
                    {{ selectedPlayers.length < 2 ? '1人以上選択してください' : 'ゲームを開始 ➡️' }}
                </button>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
    import { ref,  onMounted, computed } from 'vue';
    import { useRouter } from 'vue-router';
    import { useRoundStore } from '../stores/round';
    import { useAuthStore } from '../stores/auth';
    import type { Player } from '../types';
    import apiService from '../services/api';


    // Vue Routerのインスタンスを取得
    const router = useRouter();
    // ラウンド情報を管理するPiniaストアのインスタンスを取得
    const roundStore = useRoundStore();
    // 認証情報を管理するPiniaストアのインスタンスを取得
    const authStore = useAuthStore();
    // 新規プレイヤー名入力用のリアクティブ変数
    const newPlayerName = ref('');
    // エラーメッセージ表示用のリアクティブ変数
    const errorMessage = ref('');
    const searchQuery = ref('');

    // ログインユーザーの情報を取得
    const currentUser: Player = {
        id: authStore.getUserId,
        name: authStore.getUserName,
    };

    // 既存プレイヤーのリスト
    const existingPlayers = ref<Player[]>([]);

    const filteredPlayers = computed(() => {
      if (!searchQuery.value) {
        return existingPlayers.value;
      }
      return existingPlayers.value.filter(player =>
        player.name.toLowerCase().includes(searchQuery.value.toLowerCase())
      );
    });

    const clearSearch = () => {
      searchQuery.value = '';
    };

    const fetchCompanions = async () => {
        try {
            if (!authStore.token) {
                throw new Error('認証トークンがありません。');
            }
            const response = await apiService.getCompanions();
            // 自分自身が同伴者リストに含まれていないことを確認してから追加
            const companionExists = response.companions.some((c: Player) => c.id === currentUser.id);
            existingPlayers.value = response.companions;
            if (!companionExists) {
                existingPlayers.value.unshift(currentUser);
            }
        } catch (error) {
            if ((error as Error).message && (error as Error).message.includes('401')) {
                authStore.clearAuthInfo();
                router.push('/');
            }
            console.error(error);
        }
    };

    onMounted(async () => {
        await fetchCompanions();
    });


    // ラウンドに参加するプレイヤーのリスト
    // 初期状態でログインユーザーを選択済みとする
    const selectedPlayers = ref<Player[]>([currentUser]); 

    /**
     * 指定されたプレイヤーが現在選択されているかどうかを判定する関数
     * @param player - 判定対象のプレイヤーオブジェクト
     * @returns - 選択されていればtrue、そうでなければfalse
     */
    const isSelected = (player: Player) => {
        return selectedPlayers.value.some(p => p.id === player.id);
    };

    /**
     * プレイヤーの選択状態を切り替える関数
     * @param player - 選択状態を切り替えるプレイヤーオブジェクト
     */
    const toggleSelection = (player: Player) => {
        // ログインユーザーは選択解除できないようにする
        if (player.id === currentUser.id) return;

        if (isSelected(player)) {
            // 既に選択されている場合は、selectedPlayersから削除
            selectedPlayers.value = selectedPlayers.value.filter(p => p.id !== player.id);
        } else {
            // 選択されていない場合は、selectedPlayersに追加
            selectedPlayers.value.push(player);
        }
    };

    /**
     * 新しいプレイヤーを追加する関数
     * 入力フィールドから名前を取得し、既存プレイヤーリストと選択済みプレイヤーリストに追加する
     */
    const addNewPlayer = async () => {
        const name = newPlayerName.value.trim(); // 入力値の前後空白を削除

        // 名前が空の場合、エラーメッセージを表示して処理を中断
        if (!name) {
            errorMessage.value = 'プレイヤー名を入力してください。';
            return;
        }

        // 既存プレイヤーリストに同じ名前がないかチェック
        if (existingPlayers.value.some(p => p.name === name)) {
            errorMessage.value = `「${name}」は既に存在します。`;
            return;
        }

        // 確認ポップアップを表示
        if (!confirm(`「${name}」を追加しますか？`)) {
            return; // キャンセルされた場合は処理を中断
        }

        try {
            // エラーがない場合はメッセージをクリア
            errorMessage.value = '';

            // APIを呼び出して同伴者を追加
            const response = await apiService.addCompanion(name);

            const newPlayer: Player = {
                id: response.id, // APIからのIDを使用
                name: name,
            };
            
            existingPlayers.value.push(newPlayer); // 既存プレイヤーリストに追加
            selectedPlayers.value.push(newPlayer); // 選択済みプレイヤーリストにも追加
            newPlayerName.value = ''; // 入力フィールドをクリア
        } catch (error) {
            if ((error as any).message && (error as any).message.includes('401')) {
                authStore.clearAuthInfo();
                router.push('/');
            }
            errorMessage.value = '同伴者の追加に失敗しました。';
            console.error(error);
        }
    };

    /**
     * 選択されたプレイヤーをリストから削除する関数
     * @param player - 削除対象のプレイヤーオブジェクト
     */
    const removePlayer = (player: Player) => {
        // ログインユーザーは削除できないようにする
        if (player.id === currentUser.id) return;
        // 指定されたプレイヤーをselectedPlayersから除外して新しい配列を作成
        selectedPlayers.value = selectedPlayers.value.filter(p => p.id !== player.id);
    };

    /**
     * ゲーム開始ボタンの処理
     * 選択されたプレイヤーが1人以上いる場合、ラウンドストアにプレイヤー情報を設定し、スコア入力画面へ遷移する
     */
    const startGame = async () => {
    // 中断中のゲームがないか確認
        console.log(roundStore.roundStatus);
        if (roundStore.roundStatus === "pending"){
            if (!confirm('未保存データがあります。破棄して続行しますか？')) {
                router.push({ name: 'ScoreEntry' });
                return; // ユーザーがキャンセルした場合は処理を中断
            }
        }

         // 選択されたプレイヤーが1人以上いることを確認
        if (selectedPlayers.value.length >= 2) {
            // 選択されたプレイヤーをラウンドストアに設定
            roundStore.setPlayers(selectedPlayers.value);
            try {
                const gameId = roundStore.roundId; // UUIDを生成してgameIdとする
                const golfCourse = roundStore.course; // Get golfCourse from roundStore
                const betAmount = roundStore.wager; // Get betAmount from roundStore
                const editor = authStore.user.uid; // Get user ID from authStore
                const memo = roundStore.memo; // Get memo from roundStore

                // バックエンドにゲーム開始を通知
                await apiService.startGame({
                    gameId,
                    golfCourse,
                    betAmount,
                    players: selectedPlayers.value,
                    editor,
                    memo // Add memo to the request
                });
                console.log('Game started successfully!');
                // スコア入力画面へルーティング
                router.push({ name: 'ScoreEntry' });
            } catch (error) {
                console.error('Failed to start game:', error);
                errorMessage.value = 'ゲームの開始に失敗しました。';
            }
        }else{
            errorMessage.value = '同伴者を2人以上選択してください。';
            return
        }
    };

</script>

<style scoped>
.player-list-item {
    @apply flex items-center justify-between rounded-lg transition-all duration-200 cursor-pointer mb-2 border-2 border-transparent;
}
.player-list-item:hover {
    @apply bg-gray-50;
}

.input-field {
  @apply border border-gray-300 rounded-md px-3 py-2 w-full focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-shadow;
}



.btn-primary {
  @apply bg-green-500 text-white px-4 py-2 rounded-md hover:bg-green-600 transition-colors duration-200 whitespace-nowrap shadow-md focus:outline-none;
}

.btn-secondary {
  @apply bg-gray-200 text-gray-800 px-3 py-2 rounded-md hover:bg-gray-300 transition-colors duration-200 text-sm whitespace-nowrap focus:outline-none;
}

.remove-player-btn {
    @apply text-gray-400 hover:text-red-500 transition-colors duration-200;
}

.btn-danger {
  @apply bg-red-500 text-white px-3 py-1 rounded-md hover:bg-red-600 transition-colors duration-200 text-sm whitespace-nowrap focus:outline-none;
}

/* スクロールビューのカスタムデザイン */
.custom-scrollbar::-webkit-scrollbar {
    width: 8px;
}
.custom-scrollbar::-webkit-scrollbar-track {
    background: #f1f1f1;
    border-radius: 10px;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
    background: #a3e635;
    border-radius: 10px;
}
.custom-scrollbar::-webkit-scrollbar-thumb:hover {
    background: #84cc16;
}

.current-user-highlight {
    @apply bg-blue-50;
}
</style>