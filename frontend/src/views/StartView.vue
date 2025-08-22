<template>
<!-- メインコンテンツ部分 -->
    <div class="main-layout">
        <div class="container mx-auto max-w-sm card">
            <h1 class="text-3xl font-bold text-center text-gray-800 mb-6">
                ラウンド情報✍️
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
                    <h4 v-if="showSuggestions && golfCourseSuggestions.length" class="text-sm font-medium text-gray-700 mt-2 mb-1">近くのゴルフ場:</h4>
                    <div v-if="showSuggestions && golfCourseSuggestions.length" class="mt-1">
                        <div v-for="suggestion in golfCourseSuggestions" :key="suggestion" @click="selectSuggestion(suggestion)" class="text-xs text-blue-600 cursor-pointer hover:underline">
                            {{ suggestion }}
                        </div>
                    </div>
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
                    {{ buttonText() }}
                </button>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
    console.log('StartView.vue script setup');
    import { ref, onMounted } from 'vue';
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
    const golfCourseSuggestions = ref<string[]>([]);
    const showSuggestions = ref(false);

    const buttonText = () => {
        return roundStore.players.length ? 'スコア入力 ➡️' : '同伴者を選択 ➡️';
    };
    
    const selectCompanions = () => {
        // 過去スコア画面から遷移してきた場合考慮
        // ラウンドIDが設定されていない場合は新規ラウンドとして扱う
        if (!roundStore.players.length) {
            console.log("Setting round info for new round");
            roundStore.setRoundInfo({
            roundDate: roundDate.value,
            course: course.value,
            wager: wager.value,
            memo: memo.value,
            })
            router.push('/select-players');  
        }else{
            console.log("Setting round info for existing round");
            roundStore.setPastRoundInfo({
                // 既存のラウンドIDを保持しつつ、他の情報を更新
                roundId: roundStore.roundId,
                roundDate: roundDate.value,
                course: course.value,
                wager: wager.value,
                memo: memo.value,
            });
            router.push('/score-entry'); 
        }
    };

    // ゴルフ場名の候補を取得する関数
    async function getNearbyGolfCourseNames(lat: number, lon: number): Promise<string[]> {
        const params = new URLSearchParams({
            applicationId: "1095881049230729173", // あなたのAPP ID
            affiliateId: "15c62b88.a7bf436f.15c62b89.aa154c9f",
            format: "json",
            formatVersion: "2",
            latitude: String(lat),
            longitude: String(lon),
            searchRadius: "15", // 半径15km
            hits: "5",          // 5件取得
            sort: "distance",   // 距離順
            elements: "golfCourseName"
        });

        const url = `https://app.rakuten.co.jp/services/api/Gora/GoraGolfCourseSearch/20170623?${params}`;
        console.log("Rakuten Gora API Request URL:", url);
        const res = await fetch(url);
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json();
        console.log("Rakuten Gora API Response Data:", data);

        return (data.Items || []).map((i: any) => i.golfCourseName);
    }

    console.log('Before onMounted');

    onMounted(() => {
        console.log('Inside onMounted');
        if (navigator.geolocation) {
            console.log('Requesting geolocation...');
            navigator.geolocation.getCurrentPosition(async (position) => {
                const lat = position.coords.latitude;
                const lon = position.coords.longitude;
                console.log(`Geolocation successful: lat=${lat}, lon=${lon}`);
                try {
                    golfCourseSuggestions.value = await getNearbyGolfCourseNames(lat, lon);
                    console.log('golfCourseSuggestions:', golfCourseSuggestions.value);
                    showSuggestions.value = golfCourseSuggestions.value.length > 0;
                    console.log('showSuggestions:', showSuggestions.value);
                } catch (error) {
                    console.error("Failed to fetch golf course suggestions:", error);
                }
            }, (error) => {
                console.error("Geolocation error:", error);
            }, {
                timeout: 10000 // 10秒でタイムアウト
            });
        } else {
            console.log("Geolocation is not supported by this browser.");
        }
    });

    const selectSuggestion = (suggestion: string) => {
        course.value = suggestion;
    };

</script>

<style scoped>

</style>