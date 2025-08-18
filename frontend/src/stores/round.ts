// src/stores/round.ts
import { defineStore } from 'pinia';
import type { Player } from '../types';
import { v4 as uuidv4 } from 'uuid';

export type RoundStatus = 'initial' | 'pending' | 'completed' | 'archived';

export interface Round {
  roundId: string;
  roundDate: string;
  course: string;
  wager: string;
  memo: string;
  players: Player[];
  totalPoints: number;
  totalAmount: number;
  playerScores: { [key: string]: { points: number; amount: number; } };
  roundStatus: RoundStatus;
}

export const useRoundStore = defineStore('round', {
  state: (): Round => ({
    roundId: '',
    roundDate: '',
    course: '',
    wager: '100',
    memo: '',
    players: [],
    totalPoints: 0,
    totalAmount: 0,
    playerScores: {},
    roundStatus: 'initial',
  }),
  actions: {
    setRoundInfo(info: Partial<Round>) {
      if (!this.roundId) {
        this.roundId = uuidv4();
      }
      if (info.roundDate) this.roundDate = info.roundDate;
      if (info.course) this.course = info.course;
      if (info.wager) this.wager = info.wager;
      if (info.memo) this.memo = info.memo;
    },
    setPlayers(players: Player[]) {
      this.players = players;
    },
    setTotalPoints(points: number) {
      this.totalPoints = points;
    },
    setTotalAmount(amount: number) {
      this.totalAmount = amount;
    },
    setPlayerScore(playerName: string, points: number, amount: number) {
      this.playerScores[playerName] = { points, amount };
    },
    // ステータスを設定するアクション
    setStatus(newStatus: RoundStatus) {
      this.roundStatus = newStatus;
    },
    clearRouundInfo() {
      this.roundId = '';
      this.roundDate = '';
      this.course = '';
      this.wager = '100';
      this.memo = '';
      this.players = [];
      this.totalPoints = 0;
      this.totalAmount = 0;
      this.playerScores = {};
      this.roundStatus = 'initial';
    },
  },
  persist: {
    key: 'round-store',
    storage: localStorage
  },
});
