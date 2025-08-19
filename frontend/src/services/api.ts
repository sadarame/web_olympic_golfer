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

    // ユーザー関連のAPI
  async addCompanion(data: any): Promise<any> {
    return this.request(API_ENDPOINTS.ADD_COMPANION, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async getCompanions(token: string): Promise<any> {
    return this.request(API_ENDPOINTS.GET_COMPANIONS, {
      method: 'GET',
    });
  }

  async getUser(): Promise<any> {
    return this.request(API_ENDPOINTS.GET_USER, {
      method: 'GET',
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