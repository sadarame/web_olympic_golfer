<template>
    <!-- メインコンテンツ部分 -->
    <div class="main-layout">
        <div class="container mx-auto max-w-sm card">
            <h1 class="text-3xl font-bold text-center text-gray-800 mb-6">
                スコア入力
            </h1>

            <!-- レート設定セクション -->
            <div class="space-y-4 mb-6 p-4 bg-gray-50 rounded-xl">
                <div class="flex justify-between items-center mb-4">
                    <h2 class="text-xl font-semibold text-gray-800">レート設定</h2>
                    <span class="text-lg font-medium text-gray-700">{{ rate }}円/pt</span>
                </div>
            </div>

            <div id="player-score-sections" class="space-y-8">
                <!-- プレイヤーごとのスコア入力セクション -->
                <div v-for="player in selectedPlayers" :key="player.id" class="bg-white rounded-xl p-4 shadow-md">
                    <div class="flex justify-between items-center mb-4">
                        <h2 class="text-xl font-bold">{{ player.name }}</h2>
                        <div class="text-right">
                            <span class="text-lg font-bold text-green-600">{{ scores[player.name]?.points || 0 }}</span>
                            <span class="text-sm text-gray-500">pt</span>
                            <br>
                            <span class="text-xl font-bold text-gray-700">¥{{ (scores[player.name]?.points || 0) * rate }}</span>
                        </div>
                    </div>
                    
                    <!-- 特殊ボタン -->
                    <div class="grid grid-cols-5 gap-2 mb-4">
                        <button class="score-input-btn diamond" @click="updateScore(player.name, 10, -3)">ダイヤ</button>
                        <button class="score-input-btn gold" @click="updateScore(player.name, 5, -2)">金</button>
                        <button class="score-input-btn silver" @click="updateScore(player.name, 3, -1)">銀</button>
                        <button class="score-input-btn bronze" @click="updateScore(player.name, 1, -1)">銅</button>
                        <button class="score-input-btn iron" @click="updateScore(player.name, -1, 1)">鉄</button>
                    </div>

                    <!-- 手動入力 -->
                    <div class="flex items-center space-x-2">
                        <button class="group btn-fancy w-14 h-14 text-2xl" @click="updateManualScore(player.name, -1)">-</button>
                        <input type="number" v-model.number="scores[player.name].points" class="input-field flex-grow h-14 text-center text-2xl">
                        <button class="group btn-fancy w-14 h-14 text-2xl" @click="updateManualScore(player.name, 1)">+</button>
                    </div>
                </div>
            </div>

            <!-- 次へボタン -->
            <div class="text-center mt-8">
                <button @click="goToResult" class="btn-fancy-next">
                    結果画面へ ➡️
                </button>
            </div>
        </div>
    </div>

    <!-- カスタムアラートボックス -->
    <div v-if="showAlert" class="fixed top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 p-6 rounded-lg shadow-xl bg-white text-gray-800 z-50 text-center">
        <p class="font-bold text-lg">{{ alertMessage }}</p>
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { storeToRefs } from 'pinia';
import { useRoundStore } from '../stores/round';
import type { Player } from '../types';

const router = useRouter();
const roundStore = useRoundStore();
const { players: selectedPlayers } = storeToRefs(roundStore);


// 各プレイヤーのスコアを管理するリアクティブなオブジェクト
// 例: { "プレイヤーA": { points: 0 }, "プレイヤーB": { points: 0 } }
const scores = ref<{ [key: string]: { points: number } }>({});

// レート設定
const rate = roundStore.wager; // デフォルトレート

// カスタムアラート表示用
const showAlert = ref(false);
const alertMessage = ref('');
let alertTimeout: ReturnType<typeof setTimeout> | null = null;

// スコアを初期化する関数
const initializeScores = () => {
  selectedPlayers.value.forEach(player => {
    scores.value[player.name] = { points: 0 };
  });
};

// スコアを更新する関数（特殊ボタン用）
const updateScore = (playerName: string, scoreToAdd: number, penalty: number) => {
  if (!scores.value[playerName]) {
    scores.value[playerName] = { points: 0 };
  }
  scores.value[playerName].points += scoreToAdd;

  // 他のプレイヤーにペナルティを適用
  selectedPlayers.value.forEach(otherPlayer => {
    if (otherPlayer.name !== playerName) {
      if (!scores.value[otherPlayer.name]) {
        scores.value[otherPlayer.name] = { points: 0 };
      }
      scores.value[otherPlayer.name].points += penalty;
    }
  });
};

// スコアを更新する関数（手動入力用）
const updateManualScore = (playerName: string, change: number) => {
  if (!scores.value[playerName]) {
    scores.value[playerName] = { points: 0 };
  }
  scores.value[playerName].points += change;
};

// レート確定ボタンの処理
const setRate = () => {
  const newRate = rate.value || 0;
  rate.value = newRate;
  showAlertMessage(`レートを¥${newRate}円/ptに設定しました。`);
};

// カスタムアラートを表示する関数
const showAlertMessage = (message: string) => {
  if (alertTimeout) {
    clearTimeout(alertTimeout);
  }
  alertMessage.value = message;
  showAlert.value = true;
  alertTimeout = setTimeout(() => {
    showAlert.value = false;
    alertMessage.value = '';
  }, 2000);
};

// 結果画面へ遷移する関数
const goToResult = () => {
  showAlertMessage('結果画面へ遷移します');
  // TODO: 実際のアプリでは、この後結果画面に遷移する処理を実装
  // router.push({ name: 'ResultView' }); // 例
};

initializeScores();
</script>

<style scoped>
body {
    font-family: 'Poppins', sans-serif;
    background: linear-gradient(135deg, #c7e5a0 0%, #90d36a 100%);
    color: #333;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
}

.header {
    background-color: rgba(255, 255, 255, 0.9);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    padding: 0.75rem 1rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.card {
    background-color: rgba(255, 255, 255, 0.9);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border-radius: 1.5rem;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
    padding: 1.5rem;
    border: 1px solid rgba(255, 255, 255, 0.3);
    margin: 1rem;
}

.input-field {
    @apply w-full p-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-green-500 transition-colors duration-200;
}

.score-input-btn {
    @apply flex-grow h-14 rounded-lg text-white font-bold text-lg transition-all duration-150 transform hover:scale-105 active:scale-95;
}

.score-input-btn.diamond {
    background-color: #b9f2ff; /* A lighter blue for diamond */
    color: #000;
    text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1), 0 1px 3px rgba(0, 0, 0, 0.08);
}

.score-input-btn.gold {
    background-color: #ffd700;
    color: #8b4513;
    text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1), 0 1px 3px rgba(0, 0, 0, 0.08);
}

.score-input-btn.silver {
    background-color: #c0c0c0;
    color: #333;
    text-shadow: 1px 1px 2px rgba(255,255,255,0.4);
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1), 0 1px 3px rgba(0, 0, 0, 0.08);
}

.score-input-btn.bronze {
    background-color: #cd7f32;
    color: #fff;
    text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1), 0 1px 3px rgba(0, 0, 0, 0.08);
}

.score-input-btn.iron {
    background-color: #555;
    color: #fff;
    text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1), 0 1px 3px rgba(0, 0, 0, 0.08);
}

.btn-fancy {
    @apply relative inline-flex h-14 items-center justify-center overflow-hidden rounded-md border border-neutral-200 bg-transparent px-6 font-medium text-neutral-600 transition-all duration-100 [box-shadow:3px_3px_rgb(60_80_60)] active:translate-x-[2px] active:translate-y-[2px] active:[box-shadow:0px_0px_rgb(60_80_60)];
}

.btn-fancy-next {
    @apply w-full relative inline-flex h-14 items-center justify-center overflow-hidden rounded-md border-2 border-green-700 bg-green-500 px-6 font-bold text-white transition-all duration-100;
    box-shadow: 3px 3px rgb(20, 100, 20);
}
.btn-fancy-next:active {
    transform: translate(2px, 2px);
    box-shadow: 0px 0px rgb(20, 100, 20);
}
</style>