// src/stores/round.ts
import { defineStore } from 'pinia';
import type { Player } from '../types';
import { v4 as uuidv4 } from 'uuid';


export interface Round {
  roundId: string;
  roundDate: string;
  course: string;
  wager: string;
  memo: string;
  players: Player[];
}

export const useRoundStore = defineStore('round', {
  state: (): Round => ({
    roundId: '',
    roundDate: '',
    course: '',
    wager: '100',
    memo: '',
    players: [],
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
    clearRouundInfo() {
      this.roundId = '';
      this.roundDate = '';
      this.course = '';
      this.wager = '100';
      this.memo = '';
      this.players = [];
    },
  },
  persist: true,
});
