<template>
<!-- メインコンテンツ部分 -->
    <div class="main-layout">
        <div class="container mx-auto max-w-sm card">
            <h1 class="text-3xl font-bold text-center text-gray-800 mb-6">
                ラウンド情報を入力
            </h1>

            <!-- ラウンド基本情報入力セクション -->
            <div class="space-y-4 mb-6 text-left">
                <div>
                    <label for="round-date" class="block text-sm font-medium text-gray-700 mb-1">ラウンド日</label>
                    <input type="date" id="round-date" class="main-input" v-model="roundDate">
                </div>
                <div>
                    <label for="course-name" class="block text-sm font-medium text-gray-700 mb-1">ゴルフ場名</label>
                    <input type="text" id="course-name" class="main-input" placeholder="例: 広陵カントリークラブ" v-model="course">
                </div>
                <div>
                    <label for="bet-rate" class="block text-sm font-medium text-gray-700 mb-1">賭け金レート (1枚あたりの金額)</label>
                    <input type="number" id="bet-rate" class="main-input" v-model="wager">
                </div>
            </div>

            <!-- メモ入力セクション -->
            <div class="space-y-4 mb-6 text-left">
                <h2 class="text-xl font-semibold text-gray-800">メモ</h2>
                <textarea id="memo" rows="3" class="main-input" placeholder="ゲームに関するメモをここに記入してください。" v-model="memo"></textarea>
            </div>

            <!-- 同伴者選択ボタン -->
            <div class="text-center">
                <button id="select-partners-button" @click="selectCompanions" class="btn-solid">
                    同伴者を選択 ➡️
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

    const today = new Date();
    const yyyy = today.getFullYear();
    const mm = String(today.getMonth() + 1).padStart(2, '0'); // Months are 0-based
    const dd = String(today.getDate()).padStart(2, '0');
    const formattedToday = `${yyyy}-${mm}-${dd}`;

    const roundDate = ref(roundStore.roundDate || formattedToday);
    const course = ref(roundStore.course || '');
    const wager = ref(roundStore.wager || '100');
    const memo = ref(roundStore.memo || '');
    
    const selectCompanions = () => {
      if (!roundDate.value ) {
        alert('ラウンド日は必須です。');
        return;
      }
      roundStore.setRoundInfo({
        roundDate: roundDate.value,
        course: course.value,
        wager: wager.value,
        memo: memo.value,
      });
      router.push('/select-players');
    };
</script>

<style scoped>
    .input-base {
    @apply w-full rounded border bg-gray-50 px-3 py-2 text-gray-800 outline-none transition duration-100 ring ring-indigo-300;
    }
    /* ← バリアントは @apply に入れない */
    .input-base:focus {
    @apply ring;
    }
</style>