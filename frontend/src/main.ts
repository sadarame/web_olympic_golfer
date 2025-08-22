import { createApp } from 'vue'
import { createPinia } from 'pinia'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'
import './style.css'
import './assets/tailwind.css'
import App from './App.vue'
import router from './router'
import { auth } from './firebase'; // Import from firebase.ts
import { onAuthStateChanged } from 'firebase/auth'; // Keep this import

const app = createApp(App)
const pinia = createPinia()
pinia.use(piniaPluginPersistedstate)

app.use(pinia)
app.use(router)

// Firebase の認証状態がロードされるまで待機してからアプリをマウント
let appInitialized = false;
onAuthStateChanged(auth, (user) => {
  if (!appInitialized) {
    // useAuthStore をインポートして setAuthInfoFromFirebase を呼び出す
    import('./stores/auth').then(({ useAuthStore }) => {
      const authStore = useAuthStore();
      authStore.setAuthInfoFromFirebase(); // Firebase のユーザー情報でストアを更新
      app.mount('#app');
      appInitialized = true;
    });
  }
});