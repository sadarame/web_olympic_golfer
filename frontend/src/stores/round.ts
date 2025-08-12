// src/stores/round.ts
import { defineStore } from 'pinia';
import type { Player } from '../types';

export interface Round {
  roundDate: string;
  course: string;
  wager: string;
  memo: string;
  players: Player[];
}

export const useRoundStore = defineStore('round', {
  state: (): Round => ({
    roundDate: '',
    course: '',
    wager: '100',
    memo: '',
    players: [],
  }),
  actions: {
    setRoundInfo(info: Partial<Round>) {
      if (info.roundDate) this.roundDate = info.roundDate;
      if (info.course) this.course = info.course;
      if (info.wager) this.wager = info.wager;
      if (info.memo) this.memo = info.memo;
    },
    setPlayers(players: Player[]) {
      this.players = players;
    },
    clearRouundInfo() {
      this.roundDate = '';
      this.course = '';
      this.wager = '100';
      this.memo = '';
      this.players = [];
    },
  },
});
