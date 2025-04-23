import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '@/views/HomePage.vue'
import StatusPage from '@/views/StatusPage.vue'
import CapacityPage from '@/views/CapacityPage.vue'
import TrendPage from '@/views/TrendPage.vue'
import TablePage from '@/views/TablePage.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomePage,
  },
  {
    path: '/status',
    name: 'Status',
    component: StatusPage,
  },
  { 
    path: '/capacity', 
    name: 'Capacity', 
    component: CapacityPage },

  { 
    path: '/trend', 
    name: 'Trend', 
    component: TrendPage },
  { 
    path: '/table', 
    name: 'Table', 
    component: TablePage },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
