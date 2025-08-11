<template>
    <div>
        <AppHeader />
        <div class="flex-grow flex justify-center items-center p-4 pt-20">
            <div class="container mx-auto max-w-sm card">
                <h1 class="text-3xl font-bold text-center text-gray-800 mb-6">
                    ラウンド<br>
                    情報入力
                </h1>

                <!-- ラウンド基本情報入力セクション -->
                <div class="space-y-4 mb-6">
                    <div>
                        <label for="round-date" class="block text-sm font-medium text-gray-700 mb-1">ラウンド日</label>
                        <input type="date" id="round-date" class="input-field" v-model="roundDate">
                    </div>
                    <div>
                        <label for="course-name" class="block text-sm font-medium text-gray-700 mb-1">ゴルフ場名</label>
                        <input type="text" id="course-name" class="input-field" placeholder="例: 広陵カントリークラブ" v-model="course">
                    </div>
                    <div>
                        <label for="bet-rate" class="block text-sm font-medium text-gray-700 mb-1">賭け金レート (1枚あたりの金額)</label>
                        <input type="number" id="bet-rate" class="input-field" value="100" min="0" v-model="wager">
                    </div>
                </div>

                <!-- メモ入力セクション -->
                <div class="space-y-4 mb-6">
                    <h2 class="text-xl font-semibold text-gray-800">メモ</h2>
                    <textarea id="memo" rows="3" class="input-field" placeholder="ゲームに関するメモをここに記入してください。" v-model="memo"></textarea>
                </div>

                <!-- 同伴者選択ボタン -->
                <div class="text-center">
                    <button id="select-partners-button" @click="startGame" class="w-full group relative inline-flex h-12 items-center justify-center overflow-hidden rounded-md border border-neutral-200 bg-transparent px-6 font-medium text-neutral-600 transition-all duration-100 [box-shadow:3px_3px_rgb(60_80_60)] active:translate-x-[2px] active:translate-y-[2px] active:[box-shadow:0px_0px_rgb(60_80_60)]">
                        同伴者を選択 ➡️
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
    import { ref } from 'vue';
    import AppHeader from '../components/AppHeader.vue';

    const roundDate = ref('');
    const course = ref('');
    const wager = ref('100');
    const memo = ref('');

    const startGame = () => {
    if (!roundDate.value || !course.value) {
        alert('ラウンド日とゴルフ場は必須です。');
        return;
    }
    // 次の画面に渡すなどのロジックをここに追加
    alert(`ラウンド日: ${roundDate.value}\nゴルフ場: ${course.value}\n賭け金: ${wager.value}\nメモ: ${memo.value}`);
    };
</script>

<style scoped>
    
    .input-field {
        @apply w-full p-3 rounded-lg border border-gray-300 bg-white focus:outline-none focus:ring-2 focus:ring-green-500 transition-colors duration-200;
        background-color: white !important;
    }

    /* 遊び心を追加するアニメーション */
    @keyframes bounce-ball {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-5px); }
    }

    .golf-ball-bounce {
        animation: bounce-ball 0.8s infinite ease-in-out;
}
</style>