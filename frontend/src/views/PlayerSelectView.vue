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
                    <input type="text" id="new-player-name" class="input-field flex-grow h-12" placeholder="同伴者名を入力...">
                    <button id="add-player-button" class="group relative inline-flex h-12 items-center justify-center overflow-hidden rounded-md border border-neutral-200 bg-transparent px-6 font-medium text-neutral-600 transition-all duration-100 [box-shadow:3px_3px_rgb(60_80_60)] active:translate-x-[2px] active:translate-y-[2px] active:[box-shadow:0px_0px_rgb(60_80_60)]">
                        追加
                    </button>
                </div>
            </div>

            <!-- 既存プレイヤーリストセクション -->
            <div class="space-y-4 mb-6">
                <h2 class="text-xl font-semibold text-gray-800">登録済プレイヤーから選択</h2>
                <div id="existing-player-list" class="space-y-2 h-48 overflow-y-scroll  custom-scrollbar p-2 border border-gray-200 rounded-lg">
                    <div v-for="player in existingPlayers" :key="player.id" class="flex items-center">
                        <input type="checkbox" :id="'player-' + player.id" :value="player" v-model="selectedFriends" class="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded">
                        <label :for="'player-' + player.id" class="ml-3 block text-sm font-medium text-gray-700">{{ player.name }}</label>
                    </div>
                </div>
            </div>

            <!-- ラウンド参加メンバーリストセクション -->
            <div class="space-y-4 mb-6">
                <h2 class="text-xl font-semibold text-gray-800">ラウンドに参加する同伴者</h2>
                <div id="selected-player-list" class="space-y-2">
                    <div v-if="selectedFriends.length === 0" class="text-gray-500">
                        選択された同伴者はいません。
                    </div>
                    <div v-for="player in selectedFriends" :key="player.id" class="flex items-center justify-between bg-gray-100 p-2 rounded-md">
                        <span>{{ player.name }}</span>
                        <button @click="removeSelectedPlayer(player.id)" class="text-red-500 hover:text-red-700 text-sm">削除</button>
                    </div>
                </div>
            </div>
            
            <!-- 次へボタン -->
            <div class="text-center">
                <button id="next-button" class="btn-fancy-next" :disabled="selectedFriends.length === 0" @click="goToNextStep">
                    ゲームを開始 ➡️
                </button>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
  import { ref } from 'vue';
  import { useRouter } from 'vue-router';
  import { useRoundStore } from '../stores/round';
  import type { Player } from '../types'; // Import Player interface

  const router = useRouter();
  const roundStore = useRoundStore();

  const existingPlayers = ref<Player[]>([
    { id: 1, name: '田中 太郎' },
    { id: 2, name: '山田 花子' },
    { id: 3, name: '鈴木 一郎' },
    { id: 4, name: '佐藤 次郎' },
  ]);

  const newPlayerName = ref('');

  // Initialize selectedFriends from the store if available
  const selectedFriends = ref<Player[]>(roundStore.players || []); // Use Player interface

  const addNewPlayer = () => {
    if (newPlayerName.value.trim() === '') {
      alert('同伴者名を入力してください。');
      return;
    }
    const newName = newPlayerName.value.trim();
    if (existingPlayers.value.some(player => player.name === newName)) {
      alert('その同伴者は既に登録されています。');
      return;
    }

    const newId = Math.max(...existingPlayers.value.map(p => p.id), 0) + 1;
    const newPlayer: Player = { id: newId, name: newName };

    existingPlayers.value.push(newPlayer);
    selectedFriends.value.push(newPlayer); // Automatically select the new player
    newPlayerName.value = ''; // Clear input
  };

  const removeSelectedPlayer = (playerId: number) => {
    selectedFriends.value = selectedFriends.value.filter(player => player.id !== playerId);
  };

  const goToNextStep = () => {
    if (selectedFriends.value.length === 0) {
      alert('同伴者を一人以上選択してください。');
      return;
    }
    roundStore.setPlayers(selectedFriends.value);
    // Navigate to the next step, e.g., score entry
    router.push('/score-entry'); // Assuming a new route for score entry
  };
</script>

<style scoped>
        /* プレイヤーリストアイテムのデザイン */
        .player-list-item {
            /* flex items-center justify-between p-3 bg-white rounded-lg shadow-sm transition-all duration-200 cursor-pointer; */
            margin-bottom: 0.5rem;
            border: 2px solid transparent;
        }
        .player-list-item:hover {
            background-color: #f9fafb; /* bg-gray-50 */
        }
        .player-list-item.selected {
            background-color: #dcfce7; /* bg-green-100 */
            border-color: #22c55e; /* border-green-500 */
            box-shadow: 0 0 0 2px #22c55e; /* ring-2 ring-green-500 */
        }
        .player-list-item.selected:hover {
            background-color: #bbf7d0; /* bg-green-200 */
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
