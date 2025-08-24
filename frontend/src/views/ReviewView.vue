<template>
  <div class="main-layout">
    <div class="container mx-auto p-4 md:p-8 max-w-md card">
      <h1 class="text-3xl font-bold text-center mb-6 text-gray-800">レビュー ⭐️</h1>

      <div class="space-y-8">
        <!-- レビュー投稿フォーム -->
        <div>
          <h2 class="text-xl font-semibold mb-4 text-gray-700">あなたのレビューを投稿する</h2>
          <form @submit.prevent="submitReview">
            <div class="mb-4">
              <label for="rating" class="block text-gray-700 text-sm font-bold mb-2">評価:</label>
              <select id="rating" v-model="newReview.rating"
                class="shadow border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                required>
                <option value="">選択してください</option>
                <option value="5">⭐️⭐️⭐️⭐️⭐️ (最高)</option>
                <option value="4">⭐️⭐️⭐️⭐️ (良い)</option>
                <option value="3">⭐️⭐️⭐️ (普通)</option>
                <option value="2">⭐️⭐️ (悪い)</option>
                <option value="1">⭐️ (最低)</option>
              </select>
            </div>
            <div class="mb-4">
              <label for="comment" class="block text-gray-700 text-sm font-bold mb-2">コメント:</label>
              <textarea id="comment" v-model="newReview.comment" rows="5"
                class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                placeholder="アプリの感想や改善点などをご記入ください"></textarea>
            </div>
            <button type="submit"
              class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline">
              レビューを送信
            </button>
          </form>
        </div>

        <!-- 既存レビュー表示 -->
        <div class="pb-8 border-t-4 border-gray-300 pt-8">
          <h2 class="text-xl font-semibold mb-4 text-gray-700">みんなのレビュー</h2>
          <div v-if="reviews.length === 0" class="text-gray-600 text-center">
            <p>まだレビューがありません。最初のレビューを投稿してみませんか？</p>
          </div>
          <div v-else>
            <div v-for="review in reviews" :key="review.id"
              class="border-b pb-4 mb-4 last:border-b-0 last:pb-0 last:mb-0">
              <div class="flex items-center mb-2">
                <span class="font-bold text-lg text-yellow-500">{{ '⭐️'.repeat(review.rating) }}</span>
                <span class="ml-2 text-gray-600 text-sm">{{ review.userName || '匿名ユーザー' }}</span>
                <span class="ml-auto text-gray-500 text-xs">{{ formatDate(review.createdAt) }}</span>
              </div>
              <p class="text-gray-800">{{ review.comment }}</p>
            </div>
          </div>
        </div>


      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { apiService } from '../services/api';
import { useAuthStore } from '../stores/auth';

interface Review {
  id?: string;
  userId: string;
  userName?: string;
  rating: number;
  comment: string;
  createdAt?: string;
}

const authStore = useAuthStore();
const reviews = ref<Review[]>([]);
const newReview = ref<Review>({
  userId: authStore.user?.uid || '',
  userName: authStore.user?.customName || authStore.user?.name || '',
  rating: 0,
  comment: '',
});

const fetchReviews = async () => {
  try {
    const response = await apiService.getReviews();
    reviews.value = response.reviews.map((r: any) => ({
      id: r.id,
      userId: r.userId,
      userName: r.userName || '匿名ユーザー',
      rating: r.rating,
      comment: r.comment,
      createdAt: r.createdAt,
    }));
  } catch (error) {
    console.error("レビューの取得に失敗しました:", error);
    alert("レビューの読み込み中にエラーが発生しました。");
  }
};

const submitReview = async () => {
  if (!authStore.isAuthenticated) {
    alert("レビューを投稿するにはログインが必要です。");
    return;
  }
  if (newReview.value.rating === 0) {
    alert("評価を選択してください。");
    return;
  }

  try {
    // Ensure userId and userName are up-to-date before submission
    newReview.value.userId = authStore.user?.uid || '';
    newReview.value.userName = authStore.user?.customName || authStore.user?.name || '';

    await apiService.submitReview(newReview.value);
    alert("レビューが正常に投稿されました！");
    newReview.value.rating = 0;
    newReview.value.comment = '';
    fetchReviews(); // レビューリストを更新
  } catch (error) {
    console.error("レビューの投稿に失敗しました:", error);
    alert("レビューの投稿中にエラーが発生しました。");
  }
};

const formatDate = (dateString?: string) => {
  if (!dateString) return '';
  const date = new Date(dateString);
  return date.toLocaleDateString('ja-JP', { year: 'numeric', month: 'long', day: 'numeric' });
};

onMounted(() => {
  fetchReviews();
});
</script>

<style scoped>
/* Tailwind CSS is used for most styling, but custom styles can be added here if needed */
</style>
