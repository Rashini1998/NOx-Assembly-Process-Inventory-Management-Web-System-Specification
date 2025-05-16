import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '@/views/HomePage.vue'
import StatusPage from '@/views/StatusPage.vue'
import CapacityPage from '@/views/CapacityPage.vue'
import TrendPage from '@/views/TrendPage.vue'
import GeneralPurposePage from '@/views/GeneralPurposePage.vue'
import IMM_Setting from '@/views/IMM_SettingScreen.vue'
import HelpScreen from '@/views/HelpScreen.vue'

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
    component: CapacityPage
  },

  {
    path: '/trend',
    name: 'Trend',
    component: TrendPage
  },
  {
    path: '/general_purpose',
    name: 'General',
    component: GeneralPurposePage
  },
  {
    path: '/imm_setting',
    name: 'IMM_Setting',
    component: IMM_Setting
  },
  {
    path: '/help',
    name: 'HelpScreen',
    component: HelpScreen
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
