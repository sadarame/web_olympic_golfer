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

//TODO: 同伴者のケースを入力のケースを記載
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore();
  const isAuthenticated = authStore.getIsAuthenticated;

  if (to.name !== 'Home' && !isAuthenticated) {
    return next({ name: 'Home' });
  }

  const roundStore = useRoundStore();
  if (from.name === 'ScoreEntry' && to.name !== 'ResultView') {
    if (window.confirm('入力中のデータは失われますが、よろしいですか？')) {
      roundStore.clearRouundInfo();
      return next();
    } else {
      return next(false);
    }
  }

  next();
});

export default router;
