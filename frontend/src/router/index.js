import { createRouter, createWebHistory } from 'vue-router'
import MainPage from '../views/MainPage.vue'
import LoginPage from '../views/LoginPage.vue'
import UserMain from '../views/UserMain.vue'
import ViewCustomerStocks from '../views/ViewCustomerStocks.vue'
import BuySellStocks from '../views/BuySellStocks.vue'
import ManagePortfolio from '../views/ManagePortfolio.vue'
import PortfolioEvaluation from '../views/PortfolioEvaluation.vue'
import CustomerProfile from '../views/CustomerProfile.vue'
import ViewStockOrder from '../views/ViewStockOrder.vue'

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
    path: "/ViewStockOrder",
    name: "ViewStockOrder",
    component: ViewStockOrder,
    meta: {
      title: "ViewStockOrder",
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

  {
    path: "/ManagePortfolio",
    name: "ManagePortfolio",
    component: ManagePortfolio,
    meta: {
      title: "ManagePortfolio",
      requiresAuth: false,
    }
  },

  {
    path: "/PortfolioEvaluation/:portfolioid",
    name: "PortfolioEvaluation",
    component: PortfolioEvaluation,
    meta: {
      title: "PortfolioEvaluation",
      requiresAuth: false,
    }
  },

  {
    path: "/CustomerProfile",
    name: "CustomerProfile",
    component: CustomerProfile,
    meta: {
      title: "CustomerProfile",
      requiresAuth: false,
    }
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
