<template>
  <div class="main-layout">
    <div class="container mx-auto p-4 md:p-8 max-w-lg card">
      <h2 class="text-2xl font-bold text-center mb-6">スコア入力</h2>
      <!-- ラウンド情報表示 -->
      <div class="mb-6 p-4 bg-gray-100 rounded-md">
        <p><strong>ラウンド日:</strong> {{ roundStore.roundDate }}</p>
        <p><strong>ゴルフ場:</strong> {{ roundStore.course }}</p>
        <p><strong>賭け金:</strong> {{ roundStore.wager }}</p>
        <p><strong>メモ:</strong> {{ roundStore.memo }}</p>
      </div>

      <!-- プレイヤーとスコア入力 -->
      <div class="space-y-4">
        <div v-for="player in roundStore.players" :key="player.id" class="border p-3 rounded-md">
          <h3 class="font-semibold text-lg mb-2">{{ player.name }}</h3>
          <div class="grid grid-cols-6 gap-2">
            <div v-for="hole in 18" :key="hole" class="text-center">
              <label :for="`player-${player.id}-hole-${hole}`" class="block text-xs text-gray-600">H{{ hole }}</label>
              <input type="number" :id="`player-${player.id}-hole-${hole}`" class="score-input-field" v-model="playerScores[player.id][hole]">
            </div>
          </div>
        </div>
      </div>

      <div class="mt-8 text-center">
        <button @click="saveScores" class="w-full group relative inline-flex h-12 items-center justify-center overflow-hidden rounded-md border border-neutral-200 bg-transparent px-6 font-medium text-neutral-600 transition-all duration-100 [box-shadow:3px_3px_rgb(60_80_60)] active:translate-x-[2px] active:translate-y-[2px] active:[box-shadow:0px_0px_rgb(60_80_60)]">
          スコアを保存
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

// Initialize playerScores with a structure to hold scores for each player and hole
const playerScores = ref<{ [playerId: number]: { [hole: number]: number | null } }>({});

// Initialize scores for existing players
roundStore.players.forEach(player => {
  playerScores.value[player.id] = {};
  for (let i = 1; i <= 18; i++) {
    playerScores.value[player.id][i] = null; // Or 0, depending on desired initial state
  }
});

const saveScores = () => {
  console.log('Saving scores:', playerScores.value);
  // Here you would typically send the scores to a backend or save them locally
  alert('スコアが保存されました！');
  // Optionally, navigate back to home or a summary page
  router.push('/');
};
</script>

<style scoped>
.score-input-field {
  @apply w-full p-1 text-sm rounded border bg-gray-50 text-center outline-none ring-indigo-300 transition duration-100 focus:ring;
}
</style>
