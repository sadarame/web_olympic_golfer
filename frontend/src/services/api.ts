import { getApiUrl, getAuthHeaders, API_ENDPOINTS } from '../config/api';

// API呼び出しの基本クラス
class ApiService {
  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = getApiUrl(endpoint);
    const response = await fetch(url, {
      ...options,
      headers: {
        ...getAuthHeaders(),
        ...options.headers,
      },
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.message || `HTTP error! status: ${response.status}`);
    }

    return response.json();
  }

  // ゲーム関連のAPI
  async startGame(data: any, token?: string): Promise<any> {
    return this.request(API_ENDPOINTS.START_GAME, {
      method: 'POST',
      body: JSON.stringify(data),
      headers: getAuthHeaders(token),
    });
  }

  async updateScore(data: any, token?: string): Promise<any> {
    return this.request(API_ENDPOINTS.UPDATE_SCORE, {
      method: 'POST',
      body: JSON.stringify(data),
      headers: getAuthHeaders(token),
    });
  }

  async getGameList(token?: string): Promise<any> {
    return this.request(API_ENDPOINTS.GET_GAME_LIST, {
      method: 'GET',
      headers: getAuthHeaders(token),
    });
  }

  async deleteGame(gameId: string, token?: string): Promise<any> {
    return this.request(`${API_ENDPOINTS.DELETE_GAME}?gameId=${gameId}`, {
      method: 'DELETE',
      headers: getAuthHeaders(token),
    });
  }

  async getGameInfo(gameId: string, token?: string): Promise<any> {
    return this.request(`${API_ENDPOINTS.GET_GAME_INFO}?gameId=${gameId}`, {
      method: 'GET',
      headers: getAuthHeaders(token),
    });
  }

  // ユーザー関連のAPI
  async registerUser(data: any, token: string): Promise<any> {
    return this.request(API_ENDPOINTS.REGISTER_USER, {
      method: 'POST',
      body: JSON.stringify(data),
      headers: getAuthHeaders(token),
    });
  }

    // ユーザー関連のAPI
  async addCompanion(data: any, token: string): Promise<any> {
    return this.request(API_ENDPOINTS.REGISTER_USER, {
      method: 'POST',
      body: JSON.stringify(data),
      headers: getAuthHeaders(token),
    });
  }

  async getUser(token: string): Promise<any> {
    return this.request(API_ENDPOINTS.GET_USER, {
      method: 'GET',
      headers: getAuthHeaders(token),
    });
  }

  // ヘルスチェック
  async healthCheck(): Promise<any> {
    return this.request(API_ENDPOINTS.HEALTH, {
      method: 'GET',
    });
  }
}

// シングルトンインスタンスをエクスポート
export const apiService = new ApiService();
export default apiService;