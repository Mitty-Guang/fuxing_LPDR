import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const routes: Array<RouteRecordRaw> = [
    {//登录界面
        path:'/',
        name:'login',
        component:()=>import(/*webpackChunkName:'Login'*/ '@/page/login/login.vue')
    },
    {//主界面
        path:'/index',
        name:'index',
        component:()=>import(/*webpackChunkName:'Index'*/ '@/page/index/index.vue'),
        redirect:'/current_vehicle',
        // 二级路由
        children:[
            {//数据分析
                path:'/data_analysis',
                name:'data_analysis',
                //component:()=>import(/*webpackChunkName:'Index'*/ '@/page/index/index.vue'),
                children:[
                    {//省份分析
                        path:'/province_analysis',
                        name:'province_analysis',
                        component:()=>import(/*webpackChunkName:'Province_analysis'*/ '@/page/data_analysis/province_analysis.vue')
                    },
                    {//车型分析
                        path:'/model_analysis',
                        name:'model_analysis',
                        component:()=>import(/*webpackChunkName:'Model_analysis'*/ '@/page/data_analysis/model_analysis.vue')
                    },
                    {//时长分析
                        path:'/time_analysis',
                        name:'time_analysis',
                        component:()=>import(/*webpackChunkName:'Time_analysis'*/ '@/page/data_analysis/time_analysis.vue')
                    },
                ]
            },
            {//车辆管理
                path:'/vehicle_management',
                name:'vehicle_management',
                //component:()=>import(/*webpackChunkName:'Index'*/ '@/page/index/index.vue'),
                children:[
                    {//当前车辆
                        path:'/current_vehicle',
                        name:'current_vehicle',
                        component:()=>import(/*webpackChunkName:'Current_vehicle'*/ '@/page/vehicle_management/current_vehicle.vue')
                    },
                    {//出入记录
                        path:'/in_out_records',
                        name:'in_out_records',
                        component:()=>import(/*webpackChunkName:'In_out_records'*/ '@/page/vehicle_management/in_out_records.vue')
                    },
                ]
            },
            {//车牌识别
                path: '/lpdr',
                name: 'lpdr',
                component:()=>import(/*webpackChunkName:'Index'*/ '@/page/lpdr/lpdr.vue'),
            }

        ]
    },

]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
