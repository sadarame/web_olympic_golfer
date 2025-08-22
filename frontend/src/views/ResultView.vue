<template>
  <div class="main-layout">
    <main class="container mx-auto max-w-sm card">
      <!-- ページタイトル -->
      <h1 class="text-3xl font-bold text-center text-gray-800 mb-6">
        ラウンド結果 🏆
      </h1>

      <!-- プレイヤー結果一覧セクション -->
      <div class="space-y-4 mb-6">
        <h2 class="text-xl font-semibold text-gray-800 text-center">プレイヤー結果😎✨</h2>
        <div class="space-y-3">
          <div v-for="player in roundStore.players" :key="player.id" 
              class="bg-white rounded-xl p-4 shadow-md border-2 transition-all duration-200"
              :class="getPlayerResultClass(player.name)">
            <div class="flex justify-between items-center">
              <div class="flex items-center space-x-3">
                <span class="text-2xl">{{ getPlayerRankIcon(player.name) }}</span>
                <span class="text-lg font-semibold text-gray-800">{{ player.name }}</span>
              </div>
              <div class="text-right">
                <div class="text-sm text-gray-600">ポイント</div>
                <div class="text-xl font-bold text-green-600">{{ getPlayerPoints(player.name) }}</div>
                <div class="text-sm text-gray-600">金額</div>
                <div class="text-lg font-bold" :class="getPlayerAmountClass(player.name)">
                  ¥{{ getPlayerAmount(player.name) }}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- ラウンド基本情報セクション -->
      <div class="space-y-4 mb-6 p-4 bg-gray-50 rounded-xl shadow-md">
        <div class="flex justify-between items-center cursor-pointer" @click="toggleRoundInfo">
          <h2 class="text-xl font-semibold text-gray-800">ラウンド情報⛳️🔥</h2>
          <span class="text-lg font-medium text-gray-700">{{ showRoundInfo ? '▲' : '▼' }}</span>
        </div>
        <div v-if="showRoundInfo" class="space-y-4">
          <div class="grid grid-cols-2 gap-4 text-sm text-left">
            <div>
              <p class="text-gray-600">日付</p>
              <p class="font-semibold text-gray-800">{{ formatDate(roundStore.roundDate) }}</p>
            </div>
            <div>
              <p class="text-gray-600">レート</p>
              <p class="font-semibold text-gray-800">{{ roundStore.wager || '100' }}円/pt</p>
            </div>
          </div>
          <div class="text-sm">
            <p class="text-gray-600">ゴルフ場</p>
            <p class="font-semibold text-gray-800">{{ roundStore.course || '未設定' }}</p>
          </div>
          <div class="text-sm">
            <p class="text-gray-600">メモ</p>
            <p class="font-semibold text-gray-800">{{ roundStore.memo || 'なし' }}</p>
          </div>
        </div>
      </div>

      <!-- アクションボタンセクション -->
      <div class="space-y-4 text-center">
        <button @click="shareResults" class="w-full btn-fancy-next">
          結果を共有 📤
        </button>
        <button @click="goToHome" class="w-full btn-fancy-next">
          ホームに戻る 🏠
        </button>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
  import { ref } from 'vue';
  import { useRouter } from 'vue-router';
  import { useRoundStore } from '../stores/round';

  const router = useRouter();
  const roundStore = useRoundStore();


  // ラウンド基本情報セクションの表示/非表示を制御するref
  const showRoundInfo = ref(false);
  const toggleRoundInfo = () => {
    showRoundInfo.value = !showRoundInfo.value;
  };

  // 日付フォーマット関数
  const formatDate = (dateString: string) => {
    if (!dateString) return '未設定';
    try {
      const date = new Date(dateString);
      if (isNaN(date.getTime())) return '未設定';
      return date.toLocaleDateString('ja-JP', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      });
    } catch {
      return '未設定';
    }
  };

  // プレイヤーのポイントを取得
  const getPlayerPoints = (playerName: string) => {
    return roundStore.playerScores[playerName]?.points || 0;
  };

  // プレイヤーの金額を取得
  const getPlayerAmount = (playerName: string) => {
    return roundStore.playerScores[playerName]?.amount || 0;
  };

  // プレイヤーの金額表示クラスを取得
  const getPlayerAmountClass = (playerName: string) => {
    const amount = getPlayerAmount(playerName);
    return amount >= 0 ? 'text-green-600' : 'text-red-500';
  };

  // プレイヤーの結果表示クラスを取得
  const getPlayerResultClass = (playerName: string) => {
    const amount = getPlayerAmount(playerName);
    if (amount > 0) return 'border-green-300 bg-green-50';
    if (amount < 0) return 'border-red-300 bg-red-50';
    return 'border-gray-300';
  };

  // プレイヤーの順位アイコンを取得
  const getPlayerRankIcon = (playerName: string) => {
    const players = [...roundStore.players];
    players.sort((a, b) => {
      const aPoints = getPlayerPoints(a.name);
      const bPoints = getPlayerPoints(b.name);
      return bPoints - aPoints; // ポイントの高い順（降順）
    });
    
    const rank = players.findIndex(p => p.name === playerName) + 1;
    
    switch (rank) {
      case 1: return '🥇';
      case 2: return '🥈';
      case 3: return '🥉';
      default: return '😭';
    }
  };

  // 結果を共有
  const shareResults = async () => {
    const playerLines = roundStore.players.map(player => {
      const points = getPlayerPoints(player.name);
      const amount = getPlayerAmount(player.name);
      const rankIcon = getPlayerRankIcon(player.name);
      return `${rankIcon} ${player.name}: ${points}pt (${amount >= 0 ? '+' : ''}${amount}円)`;
    });

    const resultsSummary = [
      '⛳️ Olympic Golfer ラウンド結果 🏆',
      playerLines.join('\n'),
      '',
      '---ラウンド情報 ---',
      `日付: ${formatDate(roundStore.roundDate)}`,
      `レート: ${roundStore.wager || '100'}円/pt`,
      `ゴルフ場: ${roundStore.course || '未設定'}`,
      `メモ: ${roundStore.memo || 'なし'}`,
      '',
      '#OlympicGolfer #ゴルフ'
    ].join('\n');

    if (navigator.share) {
      try {
        await navigator.share({
          title: 'Olympic Golfer ラウンド結果',
          text: resultsSummary,
        });
        console.log('Results shared successfully!');
      } catch (error) {
        console.error('Error sharing results:', error);
      }
    } else {
      // Fallback: Copy to clipboard
      try {
        await navigator.clipboard.writeText(resultsSummary);
        alert('結果をクリップボードにコピーしました！');
      } catch (error) {
        console.error('Error copying to clipboard:', error);
        alert('結果のコピーに失敗しました。手動でコピーしてください。');
      }
    }
  };

  // ホームに戻る
  const goToHome = () => {
    roundStore.clearRouundInfo();
    router.push('/');
  };
</script>

<style scoped>
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

.btn-fancy-next {
  @apply w-full relative inline-flex h-14 items-center justify-center overflow-hidden rounded-md border-2 border-green-700 bg-green-500 px-6 font-bold text-white transition-all duration-100;
  box-shadow: 3px 3px rgb(20, 100, 20);
}

.btn-fancy-next:active {
  transform: translate(2px, 2px);
  box-shadow: 0px 0px rgb(20, 100, 20);
}

.btn-outline {
  @apply relative inline-flex h-12 items-center justify-center overflow-hidden rounded-md border border-neutral-200 bg-transparent px-6 font-medium text-neutral-600 transition-all duration-100 shadow-[3px_3px_rgb(60_80_60)] active:translate-x-[2px] active:translate-y-[2px] active:shadow-[0px_0px_rgb(60_80_60)];
}
</style>
