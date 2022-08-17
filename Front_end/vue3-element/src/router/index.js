import {createRouter,createWebHashHistory} from "vue-router"

const routes = [
    {//登录界面
        path:'/',
        name:'login',
        component:()=>import(/*webpackChunkName:'Login'*/ '@/page/login/login.vue')
    },
    {//主界面
        path:'/index',
        name:'index',
        component:()=>import(/*webpackChunkName:'Index'*/ '@/page/index/index.vue')
    }
]

const router = createRouter({
  // 内部提供了 history 模式的实现。为了简单起见，我们在这里使用 hash 模式。
  history: createWebHashHistory(),
  routes // `routes: routes` 的缩写
})

export default router