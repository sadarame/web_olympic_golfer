<template>
    <div class="flex-grow flex justify-center items-center p-4 pt-20">
        <div class="container mx-auto max-w-sm card">
            <h1 class="text-3xl font-bold text-center text-gray-800 mb-6">
                同伴者を追加
            </h1>

            <!-- 新規プレイヤー追加セクション -->
            <div class="space-y-4 mb-6">
                <h2 class="text-xl font-semibold text-gray-800">新しい同伴者を追加</h2>
                <div class="flex items-center space-x-2">
                    <input type="text" v-model="newPlayerName" @keyup.enter="addNewPlayer" class="input-field flex-grow h-12" placeholder="同伴者名を入力...">
                    <button @click="addNewPlayer" class="group btn-outline">
                        追加
                    </button>
                </div>
            </div>

            <!-- 既存プレイヤーリストセクション -->
            <div class="space-y-4 mb-6">
                <h2 class="text-xl font-semibold text-gray-800">登録済プレイヤーから選択</h2>
                <div class="space-y-2 h-48 overflow-y-scroll custom-scrollbar p-2 border border-gray-200 rounded-lg">
                    <div v-for="player in existingPlayers" :key="player.id" @click="toggleSelection(player)"
                         :class="['player-list-item', { 'selected': isSelected(player) }]">
                        <div class="flex items-center space-x-3">
                            <input type="checkbox" :checked="isSelected(player)" :disabled="player.id === 0" class="form-checkbox h-5 w-5 text-green-600 rounded-md">
                            <span class="text-gray-800 font-medium">{{ player.name }}</span>
                        </div>
                    </div>
                </div>
            </div>

            <!-- ラウンド参加メンバーリストセクション -->
            <div class="space-y-4 mb-6">
                <h2 class="text-xl font-semibold text-gray-800">ラウンドに参加する同伴者</h2>
                <div class="space-y-2">
                    <div v-for="player in selectedPlayers" :key="player.id" class="player-list-item">
                        <span class="text-gray-800 font-medium">{{ player.name }}</span>
                        <button @click="removePlayer(player)" :disabled="player.id === 0" class="remove-player-btn">
                            ×
                        </button>
                    </div>
                </div>
            </div>
            
            <!-- 次へボタン -->
            <div class="text-center">
                <button @click="startGame" :disabled="selectedPlayers.length < 1" class="btn-solid">
                    {{ selectedPlayers.length < 1 ? '同伴者を1人以上選択してください' : 'ゲームを開始 ➡️' }}
                </button>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import { useRoundStore } from '../stores/round';
import type { Player } from '../types';

// Vue Routerのインスタンスを取得
const router = useRouter();
// ラウンド情報を管理するPiniaストアのインスタンスを取得
const roundStore = useRoundStore();

// 新規プレイヤー名入力用のリアクティブ変数
const newPlayerName = ref('');

// 既存プレイヤーのリスト（テストデータ）
// 実際のアプリケーションでは、APIなどから取得する
const existingPlayers = ref<Player[]>([
  { id: 0, name: 'ログインユーザー' }, // ID 0 をログインユーザーとして扱う
  { id: 1, name: '田中 太郎' },
  { id: 2, name: '山田 花子' },
  { id: 3, name: '鈴木 一郎' },
  { id: 4, name: '佐藤 次郎' },
]);

// ラウンドに参加するプレイヤーのリスト
// 初期状態でログインユーザーを選択済みとする
const selectedPlayers = ref<Player[]>([{ id: 0, name: 'ログインユーザー' }]); 

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
  // ログインユーザー（ID 0）は選択解除できないようにする
  if (player.id === 0) return;

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
const addNewPlayer = () => {
  const name = newPlayerName.value.trim(); // 入力値の前後空白を削除
  // 名前が空でなく、かつ既存プレイヤーリストに同じ名前がない場合のみ追加
  if (name && !existingPlayers.value.some(p => p.name === name)) {
    const newPlayer: Player = {
      id: Date.now(), // ユニークなIDを生成（簡易的な方法）
      name: name,
    };
    existingPlayers.value.push(newPlayer); // 既存プレイヤーリストに追加
    selectedPlayers.value.push(newPlayer); // 選択済みプレイヤーリストにも追加
    newPlayerName.value = ''; // 入力フィールドをクリア
  }
};

/**
 * 選択されたプレイヤーをリストから削除する関数
 * @param player - 削除対象のプレイヤーオブジェクト
 */
const removePlayer = (player: Player) => {
  // ログインユーザー（ID 0）は削除できないようにする
  if (player.id === 0) return;
  // 指定されたプレイヤーをselectedPlayersから除外して新しい配列を作成
  selectedPlayers.value = selectedPlayers.value.filter(p => p.id !== player.id);
};

/**
 * ゲーム開始ボタンの処理
 * 選択されたプレイヤーが1人以上いる場合、ラウンドストアにプレイヤー情報を設定し、スコア入力画面へ遷移する
 */
const startGame = () => {
  // 選択されたプレイヤーが1人以上いることを確認
  if (selectedPlayers.value.length >= 1) {
    // ラウンドストアに選択されたプレイヤー情報を設定
    roundStore.setPlayers(selectedPlayers.value);
    // スコア入力画面へルーティング
    router.push({ name: 'ScoreEntry' });
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
.player-list-item.selected {
    /* @apply bg-green-100 border-green-500 ring-2 ring-green-500; */
}
.player-list-item.selected:hover {
    /* @apply bg-green-200; */
}

.input-field {
    @apply border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent;
}

.btn-outline {
    @apply relative inline-flex h-12 items-center justify-center overflow-hidden rounded-md border border-neutral-200 bg-transparent px-6 font-medium text-neutral-600 transition-all duration-100 shadow-[3px_3px_rgb(60_80_60)] active:translate-x-[2px] active:translate-y-[2px] active:shadow-[0px_0px_rgb(60_80_60)];
}

.btn-solid {
    @apply w-full relative inline-flex h-12 items-center justify-center overflow-hidden rounded-md border-2 border-green-700 bg-green-500 px-6 font-bold text-white transition-all duration-100 shadow-[3px_3px_rgb(20_100_20)] active:translate-x-[2px] active:translate-y-[2px] active:shadow-[0px_0px_rgb(20_100_20)];
}

.remove-player-btn {
    @apply text-gray-400 hover:text-red-500 transition-colors duration-200;
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
</style>