// API設定
const API_CONFIG = {
  // 開発環境（Firebase Emulator）
  development: {
    baseURL: 'http://localhost:5001/olynpicgolf/us-central1',
    timeout: 10000,
  },
  // 本番環境（Firebase Functions）
  production: {
    baseURL: 'https://us-central1-olynpicgolf.cloudfunctions.net',
    timeout: 10000,
  }
};

// 現在の環境に基づいて設定を選択
const currentEnv = import.meta.env.MODE || 'development';
export const apiConfig = API_CONFIG[currentEnv as keyof typeof API_CONFIG];

// APIエンドポイント
export const API_ENDPOINTS = {
  // ゲーム関連
  START_GAME: '/startGame',
  UPDATE_SCORE: '/updateScoreAndGameStatus',
  GET_GAME_LIST: '/getGameList',
  DELETE_GAME: '/deleteGame',
  GET_GAME_INFO: '/getGameInfo',
  
  // ユーザー関連
  REGISTER_USER: '/registerOrUpdateUser',
  GET_USER: '/getUser',

  // コンパニオン関連
  // コンパニオン関連
  GET_COMPANIONS: '/getCompanions',
  GET_COMPANION: '/getCompanion',
  ADD_COMPANION: '/addCompanion',
  UPDATE_COMPANION: '/updateCompanion',
  // コンパニオン関連
  DELETE_COMPANION: '/deleteCompanion',
  
  // レビュー関連
  GET_REVIEWS: '/getReviews',
  SUBMIT_REVIEW: '/submitReview',
  
  // ヘルスチェック
  HEALTH: '/health',
};

// フルURLを生成するヘルパー関数
export const getApiUrl = (endpoint: string): string => {
  return `${apiConfig.baseURL}${endpoint}`;
};

// 認証ヘッダーを生成するヘルパー関数
export const getAuthHeaders = (token?: string): Record<string, string> => {
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
  };
  
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }
  
  return headers;
};
