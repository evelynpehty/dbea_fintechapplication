import { createRouter, createWebHistory } from 'vue-router'
import MainPage from '../views/MainPage.vue'
import LoginPage from '../views/LoginPage.vue'
import UserMain from '../views/UserMain.vue'
import ViewCustomerStocks from '../views/ViewCustomerStocks.vue'
import BuySellStocks from '../views/BuySellStocks.vue'

const routes = [
  {
    path: "/",
    name: "MainPage",
    component: MainPage,
    meta: {
      title: "MainPage",
      requiresAuth: false,
    }
  },
  {
    path: "/LoginPage",
    name: "LoginPage",
    component: LoginPage,
    meta: {
      title: "LoginPage",
      requiresAuth: false,
    }
  },
  {
    path: "/UserMain",
    name: "UserMain",
    component: UserMain,
    meta: {
      title: "UserMain",
      requiresAuth: false,
    }
  },
  {
    path: "/ViewCustomerStocks",
    name: "ViewCustomerStocks",
    component: ViewCustomerStocks,
    meta: {
      title: "ViewCustomerStocks",
      requiresAuth: false,
    }
  },
  {
    path: "/BuySellStocks",
    name: "BuySellStocks",
    component: BuySellStocks,
    meta: {
      title: "BuySellStocks",
      requiresAuth: false,
    }
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
