<template>
    <div class="space-y-4 mb-6 rounded-xl">
        <div class="grid grid-cols-[1fr,auto,1fr] items-center cursor-pointer" @click="toggleRoundInfo">
                        <h2 class="text-xl font-semibold text-gray-800 whitespace-nowrap">ラウンド情報⛳️🔥</h2>
            <div></div> <!-- Spacer -->
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
import { ref } from 'vue'
import { useRoundStore } from '../stores/round'

const roundStore = useRoundStore()

const showRoundInfo = ref(false)
const toggleRoundInfo = () => {
    showRoundInfo.value = !showRoundInfo.value
}

// ✅ トップレベルに定義（関数の内側に入れない）
function formatDate(value: unknown): string {
    if (!value) return '未設定'

    // Firestore Timestamp / Date / 文字列 / 数値に対応
    let d: Date | null = null
    const v = value as any
    if (typeof v?.toDate === 'function') d = v.toDate()
    else if (v instanceof Date) d = v
    else if (typeof v === 'string' || typeof v === 'number') {
        const tmp = new Date(v)
        if (!Number.isNaN(tmp.getTime())) d = tmp
    }

    return d
        ? new Intl.DateTimeFormat('ja-JP', { dateStyle: 'medium', timeZone: 'Asia/Tokyo' }).format(d)
        : '未設定'
}

// デバッグ（開発中だけ）: コンソールに 'function' と出ればOK
console.log('formatDate typeof:', typeof formatDate)
</script>

<style scoped>
/* 必要ならここに追加 */
</style>
