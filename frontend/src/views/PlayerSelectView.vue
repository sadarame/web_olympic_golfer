<template>
    <div class="flex-grow flex justify-center items-center p-4 pt-20">
        <div class="container mx-auto max-w-sm card">
            <h1 class="text-3xl font-bold text-center text-gray-800 mb-6">
                同伴者を追加
            </h1>

            <!-- 新規プレイヤー追加セクション -->
            <div class="space-y-4 mb-6">
                <h2 class="text-xl font-semibold text-gray-800">新しい同伴者を追加</h2>
                <div class="flex space-x-2">
                    <input type="text" id="new-player-name" class="input-field" placeholder="同伴者名を入力...">
                    <button id="add-player-button" class="btn-custom w-1/3">
                        追加
                    </button>
                </div>
            </div>

            <!-- 既存プレイヤーリストセクション -->
            <div class="space-y-4 mb-6">
                <h2 class="text-xl font-semibold text-gray-800">登録済プレイヤーから選択</h2>
                <div id="existing-player-list" class="space-y-2 h-48 overflow-y-scroll">
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
                <button id="next-button" class="btn-fancy-next" disabled>
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

  const router = useRouter();
  const roundStore = useRoundStore();

  const friends = ref([
    { id: 1, name: '田中 太郎' },
    { id: 2, name: '山田 花子' },
    { id: 3, name: '鈴木 一郎' },
    { id: 4, name: '佐藤 次郎' },
  ]);

  // Initialize selectedFriends from the store if available
  const selectedFriends = ref(roundStore.players || []);

  const confirmSelection = () => {
    roundStore.setPlayers(selectedFriends.value);
    router.back();
  };
</script>

<style scoped>
/* Styles are now global, so this can be empty or have component-specific styles */
</style>
