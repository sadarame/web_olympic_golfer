<template>
  <div class="main-layout">
    <div class="container mx-auto max-w-lg card">
      <h1 class="text-3xl font-bold text-center text-gray-800 mb-6">
        対戦履歴⚔️
      </h1>
      <div v-if="loading" class="text-center">
        <p>読み込み中...</p>
      </div>
      <div v-else-if="error" class="text-center text-red-500">
        <p>{{ error }}</p>
      </div>
      <div v-else-if="games.length === 0" class="text-center text-gray-500">
        <p>対戦履歴がありません。</p>
      </div>
      <div v-else class="space-y-4">
        <div v-for="game in games" :key="game.gameId" class="rounded-xl transition-all">
          <div class="flex justify-between items-center cursor-pointer" @click="toggleDetails(game.gameId)">
            <div class="w-1/2 pr-2">
              <p class="text-sm whitespace-normal">{{ game.golfCourse || '未設定のコース' }}</p>
              <p class="text-sm text-gray-500">{{ new Date(game.createdAt).toLocaleDateString() }}</p>
            </div>
            <div class="flex items-center space-x-2">
              <div class="flex flex-col items-end">
                <span :class="getStatusClass(game.status)" class="status-badge">
                  {{ getStatusText(game.status) }}
                </span>
                <span v-if="game.status === 'completed'" :class="getAmountClass(game.editorResultAmount)" class="font-bold text-lg">
                  ¥{{ game.editorResultAmount.toLocaleString() }}
                </span>

              </div>
              <div class="flex flex-col space-y-2">
                <button @click.stop="editGame(game)" class="btn-fancy text-sm h-10">
                  編集
                </button>
                <button class="btn-fancy text-sm h-10">
                  {{ expandedGameId === game.gameId ? '閉じる' : '詳細' }}
                </button>
              </div>
            </div>
          </div>
          <div v-if="expandedGameId === game.gameId" class="mt-4 pt-4 border-t border-gray-200">
            <h3 class="font-semibold text-gray-700 mb-2">プレイヤーの結果:</h3>
            <ul>
              <li v-for="player in game.players" :key="player.name" class="flex justify-between items-center py-1">
                <span>{{ player.name }}</span>
                <span :class="getAmountClass(player.amount)" class="font-bold">
                  ¥{{ player.amount.toLocaleString() }}
                </span>
              </li>
            </ul>
          </div>
        </div>
      </div>
      <div class="text-center mt-8">
        <button @click="goHome" class="btn-fancy-next">
          ホームに戻る
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import apiService from '../services/api';
import { useRoundStore } from '../stores/round';

const router = useRouter();
const roundStore = useRoundStore();
const games = ref<any[]>([]);
const loading = ref(true);
const error = ref<string | null>(null);
const expandedGameId = ref<string | null>(null);

onMounted(async () => {
  try {
    loading.value = true;
    const gameList = await apiService.getGameList();
    console.log('Fetched game list:', gameList); // デバッグログを追加
    games.value = gameList.sort((a: any, b: any) => new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime());
    error.value = null;
  } catch (err) {
    console.error('Failed to fetch game list:', err);
    error.value = 'ゲーム履歴の取得に失敗しました。';
  } finally {
    loading.value = false;
  }
});

const editGame = (game: any) => {
  roundStore.setPastRoundInfo({
    roundId: game.gameId,
    roundDate: new Date(game.createdAt).toISOString().split('T')[0],
    course: game.golfCourse,
    wager: game.wager,
    memo: game.memo,
  });

  // roundStore.setPlayers には id と name のみを持つプレイヤーオブジェクトの配列を渡す
  // ScoreEntryViewHole.vue の selectedPlayers が期待する形式
  const playersForRoundStore = game.players.map((player: any) => ({
    id: player.id || player.name, // id がない場合は name を使用
    name: player.name,
  }));
  roundStore.setPlayers(playersForRoundStore);

  // 各プレイヤーのポイントと金額を roundStore.playerScores にセット
  game.players.forEach((player: any) => {
    roundStore.setPlayerScore(player.name, player.points, player.amount);
  });

  roundStore.setStatus(game.status);
  router.push({ name: 'Start' });
};

const toggleDetails = (gameId: string) => {
  if (expandedGameId.value === gameId) {
    expandedGameId.value = null;
  } else {
    expandedGameId.value = gameId;
  }
};

const getStatusClass = (status: string) => {
  if (status === 'completed') return 'bg-green-100 text-green-800';
  if (status === 'in_progress') return 'bg-blue-100 text-blue-800';
  return 'bg-gray-100 text-gray-800';
};

const getStatusText = (status: string) => {
  if (status === 'completed') return '完了';
  if (status === 'in_progress') return '進行中';
  return '不明';
};

const getAmountClass = (amount: number) => {
  if (amount > 0) return 'text-green-600';
  if (amount < 0) return 'text-red-600';
  return 'text-gray-700';
};

const goHome = () => {
  router.push({ name: 'Home' });
};
</script>

<style scoped>
.btn-fancy {
  @apply relative inline-flex h-10 items-center justify-center overflow-hidden rounded-md border border-neutral-200 bg-transparent px-4 font-medium text-neutral-600 transition-all duration-100 [box-shadow:2px_2px_rgb(60_80_60)] active:translate-x-[1px] active:translate-y-[1px] active:[box-shadow:0px_0px_rgb(60_80_60)];
}
.btn-fancy-next {
  @apply w-full relative inline-flex h-14 items-center justify-center overflow-hidden rounded-md border-2 border-green-700 bg-green-500 px-6 font-bold text-white transition-all duration-100;
  box-shadow: 3px 3px rgb(20, 100, 20);
}
.btn-fancy-next:active {
  transform: translate(2px, 2px);
  box-shadow: 0px 0px rgb(20, 100, 20);
}
.status-badge {
  @apply text-xs font-semibold inline-block py-1 px-2 uppercase rounded-full;
}
</style>
