import { defineStore } from 'pinia';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    isAuthenticated: false,
    user: null as any | null, // user オブジェクトに customName を含める
    token: null as string | null,
  }),
  actions: {
    // setAuthInfo で customName も受け取るように変更
    setAuthInfo(user: any, token: string, customName?: string) {
      this.isAuthenticated = true;
      this.user = { ...user, customName: customName || user.name }; // customName があればそれを使う、なければuser.name
      this.token = token;
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
    getUserName: (state) => state.user?.customName || state.user?.name || '',
    getUserId: (state) => state.user?.id || null,
    getToken: (state) => state.token,
    getIsAuthenticated: (state) => state.isAuthenticated,
  },
  persist: true,
});