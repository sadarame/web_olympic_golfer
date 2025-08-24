<template>
    <div class="space-y-4 mb-6 p-4 bg-gray-50 rounded-xl shadow-md">
        <div class="grid grid-cols-[1fr,auto,1fr] items-center cursor-pointer" @click="toggleRoundInfo">
            <div></div> <!-- Spacer -->
            <div class="text-xl font-semibold text-gray-800">ラウンド情報⛳️🔥</div>
            <span class="text-lg font-medium text-gray-700 justify-self-end">{{ showRoundInfo ? '▲' : '▼' }}</span>
        </div>
        <div v-if="showRoundInfo" class="space-y-4 text-left pl-2">
            <div class="grid grid-cols-2 gap-4 text-sm">
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
</template>

<script setup lang="ts">
    import { useRoundStore } from '../stores/round';
    import { ref } from 'vue';

    const roundStore = useRoundStore();

    const showRoundInfo = ref(false);
    const toggleRoundInfo = () => {
        showRoundInfo.value = !showRoundInfo.value;

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
};
</script>


<style scoped>
/* Add any specific styles for this component here if needed */
</style>