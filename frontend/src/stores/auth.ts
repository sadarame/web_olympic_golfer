import { defineStore } from 'pinia';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    isAuthenticated: false,
    user: null as any | null,
    token: null as string | null,
  }),
  actions: {
    setAuthInfo(user: any, token: string) {
      this.isAuthenticated = true;
      this.user = user;
      this.token = token;
    },
    clearAuthInfo() {
      this.isAuthenticated = false;
      this.user = null;
      this.token = null;
    },
    // ユーザー名を更新するアクションを追加
    updateUserName(newName: string) {
      if (this.user) {
        this.user.name = newName;
      }
    },
  },
  getters: {
    getUser: (state) => state.user,
    getToken: (state) => state.token,
    getIsAuthenticated: (state) => state.isAuthenticated,
  },
  persist: true,
});