<template>
  <div class="main-layout">
    <div class="container p-4 mx-auto max-w-sm card">
      <h1 class="text-3xl font-bold text-center mb-6 text-gray-800">友達管理 🤝</h1>

      <div class="space-y-6 mb-6 text-left">
        <!-- 友達追加フォーム -->
        <div>
          <h2 class="text-xl font-semibold text-gray-700 mb-4">新しい友達を追加👯‍♂️</h2>
          <div class="flex flex-col gap-2">
            <input 
              v-model="newCompanionName" 
              placeholder="新しい友達の名前" 
              class="input-field flex-grow"
            >
            <button @click="addCompanion" class="btn-solid">
              追加
            </button>
          </div>
          <p v-if="companionError" class="text-red-500 text-sm mt-2">{{ companionError }}</p>
        </div>
        <!-- 友達リスト & 検索 -->
        <div>
          <h2 class="text-xl font-semibold text-gray-700 mb-4">友達リスト😎</h2>
          <div class="flex items-center gap-2 mb-4">
            <input 
              v-model="searchQuery" 
              placeholder="名前で検索..." 
              class="input-field w-full"
            >
            <button @click="clearSearch" class="btn-secondary">クリア</button>
          </div>
          
          <div class="space-y-3">
              <ul v-if="filteredCompanions.length > 0" class="space-y-3">
                <li v-for="companion in filteredCompanions" :key="companion.id" class="flex items-center justify-between bg-white p-3 rounded-lg shadow-sm border border-gray-200">
                  <span class="text-gray-800 font-medium px-1">{{ companion.name }}</span>
                  <div class="flex items-center gap-2">
                    <router-link :to="`/friends/${companion.id}`" class="btn-secondary">
                      編集
                    </router-link>
                    <button @click="deleteCompanion(companion.id)" class="btn-danger">
                      削除
                    </button>
                  </div>
                </li>
              </ul>
              <div v-else class="text-center text-gray-500 py-8">
                <p>まだ友達が登録されていません。</p>
              </div>
          </div>
        </div>
      </div>
      
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { getCompanions, addCompanion as apiAddCompanion, deleteCompanion as apiDeleteCompanion } from '@/services/api';

interface Companion {
  id: string;
  name: string;
}

const companions = ref<Companion[]>([]);
const newCompanionName = ref('');
const searchQuery = ref('');
const companionError = ref('');

const filteredCompanions = computed(() => {
  return companions.value.filter(companion =>
    companion.name.toLowerCase().includes(searchQuery.value.toLowerCase())
  );
});

const clearSearch = () => {
  searchQuery.value = '';
};

const fetchCompanions = async () => {
  try {
    const response = await getCompanions();
    companions.value = response.companions;
  } catch (error) {
    console.error('Failed to fetch companions:', error);
  }
};

const addCompanion = async () => {
  companionError.value = ''; // Clear previous errors
  if (!newCompanionName.value.trim()) {
    companionError.value = '名前を入力してください。';
    return;
  }

  const isDuplicate = companions.value.some(
    (c) => c.name.toLowerCase() === newCompanionName.value.trim().toLowerCase()
  );

  if (isDuplicate) {
    companionError.value = 'この名前の友達はすでに登録されています。';
    return;
  }

  try {
    const response = await apiAddCompanion(newCompanionName.value.trim());
    companions.value.push(response.companion);
    newCompanionName.value = '';
  } catch (error) {
    console.error('Failed to add companion:', error);
    companionError.value = '友達の追加に失敗しました。';
  }
};

const deleteCompanion = async (companionId: string) => {
  if (confirm('本当にこの友達を削除しますか？')) {
    try {
      await apiDeleteCompanion(companionId);
      companions.value = companions.value.filter(c => c.id !== companionId);
    } catch (error) {
      console.error('Failed to delete companion:', error);
      alert('友達の削除に失敗しました。'); // Optional: provide user feedback on failure
    }
  }
};

onMounted(() => {
  fetchCompanions();
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
  @apply bg-transparent border-2 border-green-500 text-green-600 font-semibold px-3 py-2 rounded-md hover:bg-green-50 hover:text-green-700 transition-colors duration-200 text-sm whitespace-nowrap focus:outline-none;
}

.btn-danger {
  @apply bg-red-500 text-white px-3 py-1 rounded-md hover:bg-red-600 transition-colors duration-200 text-sm whitespace-nowrap;
}
</style>