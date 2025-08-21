import { getApiUrl, API_ENDPOINTS } from '../config/api';
import router from '../router';
import { useAuthStore } from '../stores/auth';
import { auth } from '../main'; // Firebase auth インスタンスをインポート

// API呼び出しの基本クラス
class ApiService {
  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = getApiUrl(endpoint);
    
    // 認証ヘッダーを動的に取得
    const authHeaders = await this.getAuthHeaders();

    // デバッグ用ログの追加: リクエスト情報を表示
    console.log('API Request:', {
      url: url,
      method: options.method || 'GET',
      headers: { ...authHeaders, ...options.headers },
      body: options.body ? JSON.parse(options.body.toString()) : undefined,
    });

    const response = await fetch(url, {
      ...options,
      headers: {
        ...authHeaders,
        ...options.headers,
      },
    });

    // デバッグ用ログの追加
    console.log('API Response:', response);
    const responseText = await response.text();
    console.log('API Response Text:', responseText);

    if (!response.ok) {
      if (response.status === 401) {
        // トークン切れの場合、認証情報をクリアしてホーム画面へリダイレクト
        const authStore = useAuthStore();
        authStore.clearAuthInfo(); // clearAuth から clearAuthInfo に変更
        router.push('/');
        throw new Error('Unauthorized: Token expired or invalid.');
      }
      // エラーレスポンスがJSON形式でない場合を考慮
      try {
        const errorData = JSON.parse(responseText);
        throw new Error(errorData.message || `HTTP error! status: ${response.status}`);
      } catch (e) {
        throw new Error(`HTTP error! status: ${response.status}, Response: ${responseText}`);
      }
    }

    // レスポンスが空の場合を考慮
    if (responseText === '') {
      return {} as T; // 空のオブジェクトを返すか、適切なデフォルト値を返す
    }

    return JSON.parse(responseText); // response.json() の代わりに手動でパース
  }

  // 認証ヘッダーを生成するヘルパー関数
  private async getAuthHeaders(): Promise<Record<string, string>> {
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
    };
    
    // Firebase から最新のIDトークンを取得
    if (auth.currentUser) {
      try {
        const token = await auth.currentUser.getIdToken(true); // true を渡して強制的にトークンをリフレッシュ
        headers['Authorization'] = `Bearer ${token}`;
      } catch (error) {
        console.error("Error getting Firebase ID token:", error);
        // トークン取得失敗時は認証ヘッダーなしで続行するか、エラーをスローするか検討
        // ここではエラーをスローして、request メソッドで捕捉させる
        throw new Error("Failed to get Firebase ID token.");
      }
    }
    
    return headers;
  }

  // ゲーム関連のAPI
  async startGame(data: any): Promise<any> {
    return this.request(API_ENDPOINTS.START_GAME, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async updateScore(data: any): Promise<any> {
    return this.request(API_ENDPOINTS.UPDATE_SCORE, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  // updateScoreAndGameStatusを追加
  async updateScoreAndGameStatus(data: { gameId: string; players: any[]; status: string; }): Promise<any> {
    return this.request(API_ENDPOINTS.UPDATE_SCORE, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async getGameList(): Promise<any> {
    return this.request(API_ENDPOINTS.GET_GAME_LIST, {
      method: 'GET',
    });
  }

  async deleteGame(gameId: string): Promise<any> {
    return this.request(`${API_ENDPOINTS.DELETE_GAME}?gameId=${gameId}`, {
      method: 'DELETE',
    });
  }

  async getGameInfo(gameId: string): Promise<any> {
    return this.request(`${API_ENDPOINTS.GET_GAME_INFO}?gameId=${gameId}`, {
      method: 'GET',
    });
  }

  // ユーザー関連のAPI
  async registerUser(data: any): Promise<any> {
    return this.request(API_ENDPOINTS.REGISTER_USER, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async getUser(): Promise<any> {
    return this.request(API_ENDPOINTS.GET_USER, {
      method: 'GET',
    });
  }

  // コンパニオン関連のAPI
  async getCompanions(): Promise<any> {
    return this.request(API_ENDPOINTS.GET_COMPANIONS, {
      method: 'GET',
    });
  }

  async getCompanion(id: string): Promise<any> {
    return this.request(`${API_ENDPOINTS.GET_COMPANION}?companionId=${id}`, {
      method: 'GET',
    });
  }

  async addCompanion(name: string): Promise<any> {
    return this.request(API_ENDPOINTS.ADD_COMPANION, {
      method: 'POST',
      body: JSON.stringify({ name }),
    });
  }

  async updateCompanion(id: string, name: string, gender?: string | null, relationship?: string | null, memo?: string | null): Promise<any> {
    return this.request(`${API_ENDPOINTS.UPDATE_COMPANION}?companionId=${id}`,
     {
      method: 'PUT',
      body: JSON.stringify({ name, gender, relationship, memo }),
    });
  }

  async deleteCompanion(id: string): Promise<any> {
    return this.request(`${API_ENDPOINTS.DELETE_COMPANION}?companionId=${id}`, {
      method: 'DELETE',
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

// 外部から直接呼び出せる関数の定義
export const getCompanions = () => apiService.getCompanions();
export const getCompanion = (id: string) => apiService.getCompanion(id);
export const addCompanion = (name: string) => apiService.addCompanion(name);
export const updateCompanion = (id: string, name: string, gender?: string | null, relationship?: string | null, memo?: string | null) => apiService.updateCompanion(id, name, gender, relationship, memo);
export const deleteCompanion = (id: string) => apiService.deleteCompanion(id);

export default apiService;