import { defineStore } from 'pinia';
import { auth } from '../main'; // Firebase auth インスタンスをインポート

export const useAuthStore = defineStore('auth', {
  state: () => ({
    isAuthenticated: false,
    user: null as any | null, // user オブジェクトに customName を含める
    token: null as string | null, // Firebase ID Token
  }),
  actions: {
    // Firebase の認証状態に基づいて認証情報を設定
    async setAuthInfoFromFirebase() {
      if (auth.currentUser) {
        this.isAuthenticated = true;
        // Firebase のユーザー情報から必要なデータを取得
        const idTokenResult = await auth.currentUser.getIdTokenResult();
        this.token = idTokenResult.token;
        
        // 既存の customName を保持しつつ、Firebaseからの情報で更新
        const existingCustomName = this.user?.customName; // 既存の customName を取得
        console.log("Existing customName:", existingCustomName);

        this.user = {
          uid: auth.currentUser.uid,
          email: auth.currentUser.email,
          // displayName: auth.currentUser.displayName,
          photoURL: auth.currentUser.photoURL,
          // customName はカスタムクレームから取得するか、既存のものを保持、なければdisplayName/email
          customName: existingCustomName || auth.currentUser.displayName || auth.currentUser.email,
        };
        console.log("User info set from Firebase:", this.user, "customName:", idTokenResult.claims.customName || existingCustomName || auth.currentUser.displayName || auth.currentUser.email);
      } else {
        this.clearAuthInfo();
      }
    },
    clearAuthInfo() {
      this.isAuthenticated = false;
      this.user = null;
      this.token = null;
    },
    // customName を更新するアクション
    updateCustomName(newName: string) {
      if (this.user) {
        this.user.customName = newName;
      }
    },
  },
  getters: {
    getUser: (state) => state.user,
    getUserName: (state) => state.user?.customName || state.user?.displayName || state.user?.email || '',
    getUserId: (state) => state.user?.uid || null,
    getIsAuthenticated: (state) => state.isAuthenticated,
  },
  persist: true,
});