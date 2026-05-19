import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  { path: '/',          name: 'home',      component: () => import('@/pages/HomePage.vue') },
  { path: '/monitor',   name: 'monitor',   component: () => import('@/pages/MonitorPage.vue'),
    children: [
      { path: 'greenhouse', name: 'greenhouse', component: () => import('@/modules/greenhouse/GreenhousePanel.vue') },
      { path: 'openfield',  name: 'openfield',  component: () => import('@/modules/openfield/OpenFieldPanel.vue') },
    ]
  },
  { path: '/product',   name: 'product',   component: () => import('@/pages/ProductPage.vue') },
  { path: '/herbspirit', name: 'herbspirit', component: () => import('@/pages/HerbSpiritPage.vue'), meta: { hideFooter: true } },
  { path: '/contact',   name: 'contact',   component: () => import('@/pages/ContactPage.vue') },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    return { top: 0 }
  }
})

export default router
