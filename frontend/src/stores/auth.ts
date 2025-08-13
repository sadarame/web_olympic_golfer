import { defineStore } from 'pinia';

export const useAuthStore = defineStore('auth', {
  state: () => {
    // Attempt to load from localStorage on store initialization
    const storedUser = localStorage.getItem('user');
    const storedToken = localStorage.getItem('token');

    return {
      isAuthenticated: !!storedToken, // True if token exists
      user: storedUser ? JSON.parse(storedUser) : null,
      token: storedToken,
    };
  },
  actions: {
    setAuthInfo(user: any, token: string) {
      this.isAuthenticated = true;
      this.user = user;
      this.token = token;
      // Save to localStorage
      localStorage.setItem('user', JSON.stringify(user));
      localStorage.setItem('token', token);
    },
    clearAuthInfo() {
      this.isAuthenticated = false;
      this.user = null;
      this.token = null;
      // Remove from localStorage
      localStorage.removeItem('user');
      localStorage.removeItem('token');
    },
    // ユーザー名を更新するアクションを追加
    updateUserName(newName: string) {
      if (this.user) {
        this.user.name = newName;
        localStorage.setItem('user', JSON.stringify(this.user));
      }
    },
  },
  getters: {
    getUser: (state) => state.user,
    getToken: (state) => state.token,
    getIsAuthenticated: (state) => state.isAuthenticated,
  },
});