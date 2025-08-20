import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '../views/HomeView.vue';
import { useAuthStore } from '../stores/auth';
import { useRoundStore } from '../stores/round';

const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomeView,
  },
  {
    path: '/start',
    name: 'Start',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import('../views/StartView.vue'),
  },
  {
    path: '/select-players',
    name: 'PlayerSelect',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import('../views/PlayerSelectView.vue'),
  },
  {
    path: '/score-entry',
    name: 'ScoreEntry',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import('../views/ScoreEntryViewHole.vue'),
  },
  {
    path: '/result',
    name: 'ResultView',
    component: () => import('../views/ResultView.vue'),
  },
  {
    path: '/past-games',
    name: 'PastGamesView',
    component: () => import('../views/PastGamesView.vue'),
  },
  // Catch-all route to redirect to Home
  {
    path: '/:pathMatch(.*)*',
    redirect: '/',
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

import apiService from '../services/api'; // Add this import

router.beforeEach(async (to, from, next) => { // Mark as async
  const authStore = useAuthStore();
  const isAuthenticated = authStore.getIsAuthenticated;

  if (to.name !== 'Home' && !isAuthenticated) {
    console.log('User is not authenticated, redirecting to Home');
    return next({ name: 'Home' });

  }

  const roundStore = useRoundStore();
  if (from.name === 'ScoreEntry' && to.name !== 'ResultView' && roundStore.roundId && roundStore.roundStatus !== 'completed') {
    if (window.confirm('入力中のデータは失われますが、よろしいですか？')) {
      try {
        // Call backend to delete game from Firestore
        await apiService.deleteGame(roundStore.roundId);
        console.log('Game deleted from Firestore:', roundStore.roundId); // Add log for confirmation
      } catch (error) {
        console.error('Failed to delete game from Firestore:', error);
        // Decide how to handle deletion failure: proceed anyway, or block navigation?
        // For now, we'll proceed with clearing local data even if backend deletion fails.
      }
      roundStore.clearRouundInfo();
      if (to.name === 'Home') {
        return next();
      } else {
        return next({ name: 'Home' });
      }
    } else {
      return next(false);
    }
  }

  next();
});

export default router;
