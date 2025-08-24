<template>
  <div class="main-layout">
    <div class="container mx-auto p-4 md:p-8 max-w-md card">
      <h1 class="text-3xl font-bold text-center mb-6 text-gray-800">友達の編集 ✏️</h1>
      <div v-if="companion">
        <div class="space-y-4">
          <div class="mb-4">
            <label for="name" class="block text-gray-700 text-sm font-bold mb-2">名前:</label>
            <input id="name" v-model="companion.name" type="text" placeholder="友達の名前" class="input-field">
          </div>

          <div class="mb-4">
            <label for="gender" class="block text-gray-700 text-sm font-bold mb-2">性別:</label>
            <select id="gender" v-model="companion.gender" class="input-field">
              <option value="">選択してください</option>
              <option value="male">男性</option>
              <option value="female">女性</option>
              <option value="other">その他</option>
              <option value="unanswered">未回答</option>
            </select>
          </div>

          <div class="mb-4">
            <label for="relationship" class="block text-gray-700 text-sm font-bold mb-2">関係性:</label>
            <select id="relationship" v-model="companion.relationship" class="input-field">
              <option value="">選択してください</option>
              <option value="friend">友達</option>
              <option value="work">仕事関係</option>
              <option value="family">家族</option>
              <option value="other">その他</option>
            </select>
          </div>

          <div class="mb-4">
            <label for="memo" class="block text-gray-700 text-sm font-bold mb-2">メモ:</label>
            <textarea id="memo" v-model="companion.memo" placeholder="メモ" rows="4" class="input-field"></textarea>
          </div>
        </div>

        <div class="flex justify-end space-x-2 mt-6">
          <button @click="updateCompanion" class="btn-primary">保存</button>
          <router-link to="/friends" class="btn-secondary">戻る</router-link>
        </div>
      </div>
      <div v-else class="text-center text-gray-500 py-8">
        <p>Loading companion details...</p>
      </div>
    </div>

    <!-- Custom Alert Box -->
    <div v-if="showAlert"
        class="fixed top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 p-6 rounded-lg shadow-xl bg-white text-gray-800 z-50 text-center">
        <p class="font-bold text-lg">{{ alertMessage }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { getCompanion, updateCompanion as apiUpdateCompanion } from '@/services/api';
import type { Companion } from '@/types'; // Import Companion interface

const route = useRoute();
const router = useRouter();
const companion = ref<Companion | null>(null);

const showAlert = ref(false);
const alertMessage = ref('');
let alertTimeout: ReturnType<typeof setTimeout> | null = null;

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

const fetchCompanion = async () => {
  try {
    const companionId = route.params.id as string;
    const response = await getCompanion(companionId);
    companion.value = response.companion;
  } catch (error) {
    console.error('Failed to fetch companion:', error);
  }
};

const updateCompanion = async () => {
  if (companion.value && companion.value.name.trim()) {
    try {
      await apiUpdateCompanion(
        companion.value.id,
        companion.value.name.trim(),
        companion.value.gender || null, // Pass null if undefined or empty string
        companion.value.relationship || null,
        companion.value.memo || null
      );
      showAlertMessage('更新しました');
      setTimeout(() => {
        router.push('/friends');
      }, 2000);
    } catch (error) {
      console.error('Failed to update companion:', error);
      showAlertMessage('更新に失敗しました');
    }
  }
};

onMounted(() => {
  fetchCompanion();
});
</script>

<style scoped>
.input-field {
  @apply border border-gray-300 rounded-md px-3 py-2 w-full focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-shadow;
}

.btn-primary {
  @apply bg-blue-500 text-white px-4 py-2 rounded-md hover:bg-blue-600 transition-colors duration-200 whitespace-nowrap;
}

.btn-secondary {
  @apply bg-gray-200 text-gray-800 px-4 py-2 rounded-md hover:bg-gray-300 transition-colors duration-200 whitespace-nowrap;
}

.card {
    @apply bg-white p-6 rounded-xl shadow-md;
}
</style>
