<template>
    <!-- メインコンテンツ部分 -->
    <div class="main-layout">
        <div class="container mx-auto max-w-sm card">
            <h1 class="text-3xl font-bold text-center text-gray-800 mb-6">
                スコア入力📝
            </h1>

            <!-- レート設定セクション -->
            <div class="space-y-4 mb-6 p-2 bg-gray-50 rounded-xl shadow-md ">
                <div class="flex justify-between items-center m-2">
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
                            <!-- ポイント -->
                            <span class="text-lg font-bold text-green-600">{{ playerScores[player.name]?.points || 0 }}</span>
                            <span class="text-sm text-gray-500">pt</span>
                            <br>
                            <!-- 金額 -->
                            <span :class="['text-xl', 'font-bold', (playerScores[player.name]?.amount || 0) < 0 ? 'text-red-500' : 'text-gray-700']">¥{{ (playerScores[player.name]?.amount || 0) }}</span>
                        </div>
                    </div>
                    
                    <!-- 特殊ボタン -->
                    <div class="grid grid-cols-5 gap-2 mb-4">
                        <button v-for="button in buttonConfigs" :key="button.label" :class="['score-input-btn', button.class]" @click="updateScore(player.name, button.score)">{{ button.label }}</button>
                    </div>

                    <!-- 手動入力 -->
                    <div class="flex items-center space-x-2">
                        <button class="group btn-fancy w-14 h-14 text-2xl" @click="updateManualScore(player.name, -1)">-</button>
                        <input type="number" v-model.number="playerScores[player.name].points" class="input-field flex-grow h-14 text-center text-2xl">
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
    import { ref, computed, onMounted } from 'vue';
    import { useRouter, useRoute } from 'vue-router';
    import { storeToRefs } from 'pinia';
    import { useRoundStore } from '../stores/round';
    import type { Player } from '../types';
    
    const router = useRouter();
    const route = useRoute();
	const roundStore = useRoundStore();
	const { players: selectedPlayers, playerScores } = storeToRefs(roundStore);

    // 人数によってスコアボタンの設定を動的に生成
    // 例: 2人ならダイヤモンド3点、ゴールド2点、シルバー1点
    // 3人ならダイヤモンド4点、ゴールド3点、シルバー2点、ブロンズ1点
    // 4人以上ならダイヤモンド5点、ゴールド4点、シルバー3点、ブロンズ2 点、アイアン1点
	const buttonConfigs = computed(() => {
		const playerCount = selectedPlayers.value.length;
		let configs = [];

		// Base points for 4+ players
		let diamondPoints = 10;
		let goldPoints = 5;
		let silverPoints = 3;
		let bronzePoints = 1;
		let ironPoints = -1;

		// Adjust points based on player count
		if (playerCount === 2) {
			diamondPoints = 3;
			goldPoints = 2;
			silverPoints = 1;
		} else if (playerCount === 3) {
			diamondPoints = 4;
			goldPoints = 3;
			silverPoints = 2;
			bronzePoints = 1;
		} else if (playerCount >= 4) {
			diamondPoints = 5;
			goldPoints = 4;
			silverPoints = 3;
			bronzePoints = 2;
			ironPoints = 1; // Iron button gives 1 point for 4+ players
		}

		configs.push({ label: '💎', class: 'diamond', score: diamondPoints, penalty: -3 });
		configs.push({ label: '🥇', class: 'gold', score: goldPoints, penalty: -2 });
		configs.push({ label: '🥈', class: 'silver', score: silverPoints, penalty: -1 });

		if (playerCount >= 3) {
			configs.push({ label: '🥉', class: 'bronze', score: bronzePoints, penalty: -1 });
		}
		if (playerCount >= 4) {
			configs.push({ label: '🔩', class: 'iron', score: ironPoints, penalty: 1 });
		}

		return configs;
	});
	
    // レート設定
	const rate = roundStore.wager; 

	// カスタムアラート表示用
	const showAlert = ref(false);
	const alertMessage = ref('');
	let alertTimeout: ReturnType<typeof setTimeout> | null = null;

	// スコアを初期化する関数
	const initializeScores = () => {
        // データが存在しない場合のみ初期化
		selectedPlayers.value.forEach(player => {
            if (!playerScores.value[player.name]) {
			    roundStore.setPlayerScore(player.name, 0, 0);
                // スコア入力待ち状態に設定
                roundStore.setStatus('pending'); 
            }
		});
	};

    // TODO: 再開の場合はAPIから取得
	// スコアを更新する関数（特殊ボタン用）
    const ensurePlayer = (name: string) => {
        if (!playerScores.value[name]) {
            playerScores.value[name] = { points: 0, amount: 0 };
        }
        return playerScores.value[name];
    };

    const updateScore = (playerName: string, scoreToAdd: number) => {
        // 1) まず対象プレイヤーの存在を保証
        const ps = ensurePlayer(playerName);

        // 2) スコア加算（※ここは store 経由にしておくと永続化が確実）
        const newPoints = (ps.points || 0) + scoreToAdd;
        roundStore.setPlayerScore(playerName, newPoints, ps.amount ?? 0);

        console.log(`Updated ${playerName} points ->`, newPoints); // 値をログ出力

        // 3) 総得点
        const totalScore = selectedPlayers.value.reduce((sum, player) => {
            return sum + (ensurePlayer(player.name).points ?? 0);
        }, 0);

        console.log(`totalScore ${totalScore} `); // 値をログ出力


        // 4) 金額計算（各プレイヤーごと）
        const nPlayers = selectedPlayers.value.length;
        const numericRate = Number((rate as any)?.value ?? rate); // rateがrefでもOKに

        selectedPlayers.value.forEach(player => {
            const pPoints = ensurePlayer(player.name).points; // ★ 各人の点数
            const newAmount = (pPoints * nPlayers - totalScore) * numericRate;

            roundStore.setPlayerScore(player.name, pPoints, newAmount); // 置換更新で確実に反映
            console.log(`Calculating new amount for ${player.name} ->`, newAmount);
        });
    };


	// スコアを更新する関数（手動入力用）
	const updateManualScore = (playerName: string, change: number) => {
		const currentPoints = (playerScores.value[playerName]?.points || 0) + change;
		roundStore.setPlayerScore(playerName, currentPoints, (playerScores.value[playerName]?.amount || 0));
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