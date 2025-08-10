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
  },
  getters: {
    getUser: (state) => state.user,
    getToken: (state) => state.token,
    getIsAuthenticated: (state) => state.isAuthenticated,
  },
});
