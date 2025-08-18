import { createApp } from 'vue'
import { createPinia } from 'pinia'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'
import './style.css'
import './assets/tailwind.css'
import App from './App.vue'
import router from './router'

// Firebase のインポート
import { initializeApp } from 'firebase/app';
import { getAuth } from 'firebase/auth';

// あなたの Firebase プロジェクトの実際の値に置き換えてください
const firebaseConfig = {
  apiKey: "AIzaSyDjmSl95pxZuTpotwcS8sN6UFDFacPcz4Y",
  authDomain: "olynpicgolf.firebaseapp.com",
  projectId: "olynpicgolf",
  storageBucket: "olynpicgolf.firebasestorage.app",
  messagingSenderId: "735464206154",
  appId: "1:735464206154:web:6beade78f4d9b4c9509bb3",
  measurementId: "G-12W0MY2D42"
};

// Firebase の初期化
const firebaseApp = initializeApp(firebaseConfig);
export const auth = getAuth(firebaseApp);

const app = createApp(App)
const pinia = createPinia()
pinia.use(piniaPluginPersistedstate)

app.use(pinia)
app.use(router)

app.mount('#app')
