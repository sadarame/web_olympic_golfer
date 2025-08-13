<template>
    <div class="flex-grow flex justify-center items-center p-4 pt-20">
        <div class="container mx-auto max-w-sm card">
            <h1 class="text-3xl font-bold text-center text-gray-800 mb-6">
                同伴者を追加
            </h1>

            <!-- 新規プレイヤー追加セクション -->
            <div class="space-y-4 mb-6">
              <h2 class="text-xl font-semibold text-gray-800">新しい同伴者を追加</h2>
              <div class="flex items-center space-x-2 w-full">
                <!-- input 8割 -->
                <input
                  type="text"
                  id="new-player-name"
                  class="main-input basis-4/5 flex-none"
                  placeholder="同伴者名を入力..."
                >
                <!-- ボタン 2割 -->
                <button
                  id="add-player-button"
                  class="add-bottn"
                >
                  追加
                </button>
              </div>
            </div>

            <!-- 既存プレイヤーリストセクション -->
            <div class="space-y-4 mb-6">
                <h2 class="text-xl font-semibold text-gray-800">登録済プレイヤーから選択</h2>
                <div id="existing-player-list" class="space-y-2 h-48 overflow-y-scroll custom-scrollbar p-2 border border-gray-200 rounded-lg">
                    <!-- 既存プレイヤーリストがここに追加されます -->
                </div>
            </div>

            <!-- ラウンド参加メンバーリストセクション -->
            <div class="space-y-4 mb-6">
                <h2 class="text-xl font-semibold text-gray-800">ラウンドに参加する同伴者</h2>
                <div id="selected-player-list" class="space-y-2">
                    <!-- 選択されたプレイヤーリストがここに追加されます -->
                </div>
            </div>
            
            <!-- 次へボタン -->
            <div class="text-center">
                <button id="next-button" class="w-full relative inline-flex h-12 items-center justify-center overflow-hidden rounded-md border-2 border-green-700 bg-green-500 px-6 font-bold text-white transition-all duration-100 [box-shadow:3px_3px_rgb(20_100_20)] active:translate-x-[2px] active:translate-y-[2px] active:[box-shadow:0px_0px_rgb(20_100_20)]" disabled>
                    ゲームを開始 ➡️
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

const router = useRouter();
const roundStore = useRoundStore();

const newPlayerName = ref('');
const existingPlayers = ref<Player[]>([
  { id: 1, name: '田中 太郎' },
  { id: 2, name: '山田 花子' },
  { id: 3, name: '鈴木 一郎' },
  { id: 4, name: '佐藤 次郎' },
]);
const selectedPlayers = ref<Player[]>([]);

const isSelected = (player: Player) => {
  return selectedPlayers.value.some(p => p.id === player.id);
};

const toggleSelection = (player: Player) => {
  if (isSelected(player)) {
    selectedPlayers.value = selectedPlayers.value.filter(p => p.id !== player.id);
  } else {
    selectedPlayers.value.push(player);
  }
};

const addNewPlayer = () => {
  const name = newPlayerName.value.trim();
  if (name && !existingPlayers.value.some(p => p.name === name)) {
    const newPlayer: Player = {
      id: Date.now(), // Simple unique ID
      name: name,
    };
    existingPlayers.value.push(newPlayer);
    selectedPlayers.value.push(newPlayer);
    newPlayerName.value = '';
  }
};

const removePlayer = (player: Player) => {
  selectedPlayers.value = selectedPlayers.value.filter(p => p.id !== player.id);
};

const startGame = () => {
  if (selectedPlayers.value.length >= 1) {
    roundStore.setPlayers(selectedPlayers.value);
    router.push({ name: 'ScoreEntry' });
  }
};
</script>

<style scoped>

.add-bottom {
  @apply basis-1/5 flex-none group relative inline-flex h-12 items-center justify-center overflow-hidden rounded-md border border-neutral-200 bg-transparent px-3 font-medium text-neutral-600 transition-all duration-100 [box-shadow:3px_3px_rgb(60_80_60)] active:translate-x-[2px] active:translate-y-[2px] active:[box-shadow:0px_0px_rgb(60_80_60)]
}

.player-list-item {
    /* @apply flex items-center justify-between p-3 bg-white rounded-lg shadow-sm transition-all duration-200 cursor-pointer mb-2 border-2 border-transparent; */
}
.player-list-item:hover {
    @apply bg-gray-50;
}
.player-list-item.selected {
    /* @apply bg-green-100 border-green-500 ring-2 ring-green-500; */
}
.player-list-item.selected:hover {
    @apply bg-green-200;
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