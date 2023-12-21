import { createRouter, createWebHistory,createWebHashHistory, RouteRecordRaw } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const routes: Array<RouteRecordRaw> = [
    // {//登录界面
    //     path:'/',
    //     name:'login',
    //     component:()=>import(/*webpackChunkName:'Login'*/ '@/page/login/login.vue'),
    // },
    {//主界面
        path:'/',
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
                        component:()=>import(/*webpackChunkName:'Province_analysis'*/ '@/page/data_analysis/province_analysis.vue'),

                    },
                    {//车型分析
                        path:'/model_analysis',
                        name:'model_analysis',
                        component:()=>import(/*webpackChunkName:'Model_analysis'*/ '@/page/data_analysis/model_analysis.vue')
                    },
                    {
                        path:'/anhui',
                        name:'anhui',
                        component:()=>import(/*webpackChunkName:'anhui'*/ '@/page/data_analysis/provinces/anhui.vue')
                    },
                    {
                        path:'/beijing',
                        name:'beijing',
                        component:()=>import(/*webpackChunkName:'beijing'*/ '@/page/data_analysis/provinces/beijing.vue')
                    },
                    {
                        path:'/chongqing',
                        name:'chongqing',
                        component:()=>import(/*webpackChunkName:'chongqing'*/ '@/page/data_analysis/provinces/chongqing.vue')
                    },
                    {
                        path:'/fujian',
                        name:'fujian',
                        component:()=>import(/*webpackChunkName:'fujian'*/ '@/page/data_analysis/provinces/fujian.vue')
                    },
                    {
                        path:'/gansu',
                        name:'gansu',
                        component:()=>import(/*webpackChunkName:'gansu'*/ '@/page/data_analysis/provinces/gansu.vue')
                    },
                    {
                        path:'/guangdong',
                        name:'guangdong',
                        component:()=>import(/*webpackChunkName:'guangdong'*/ '@/page/data_analysis/provinces/guangdong.vue')
                    },
                    {
                        path:'/guangxi',
                        name:'guangxi',
                        component:()=>import(/*webpackChunkName:'guangxi'*/ '@/page/data_analysis/provinces/guangxi.vue')
                    },
                    {
                        path:'/guizhou',
                        name:'guizhou',
                        component:()=>import(/*webpackChunkName:'guizhou'*/ '@/page/data_analysis/provinces/guizhou.vue')
                    },
                    {
                        path:'/hainan',
                        name:'hainan',
                        component:()=>import(/*webpackChunkName:'hainan'*/ '@/page/data_analysis/provinces/hainan.vue')
                    },
                    {
                        path:'/hebei',
                        name:'hebei',
                        component:()=>import(/*webpackChunkName:'hebei'*/ '@/page/data_analysis/provinces/hebei.vue')
                    },
                    {
                        path:'/heilongjiang',
                        name:'heilongjiang',
                        component:()=>import(/*webpackChunkName:'heilongjiang'*/ '@/page/data_analysis/provinces/heilongjiang.vue')
                    },
                    {
                        path:'/henan',
                        name:'henan',
                        component:()=>import(/*webpackChunkName:'henan'*/ '@/page/data_analysis/provinces/henan.vue')
                    },
                    {
                        path:'/hubei',
                        name:'hubei',
                        component:()=>import(/*webpackChunkName:'hubei'*/ '@/page/data_analysis/provinces/hubei.vue')
                    },
                    {
                        path:'/hunan',
                        name:'hunan',
                        component:()=>import(/*webpackChunkName:'hunan'*/ '@/page/data_analysis/provinces/hunan.vue')
                    },
                    {
                        path:'/jiangsu',
                        name:'jiangsu',
                        component:()=>import(/*webpackChunkName:'jiangsu'*/ '@/page/data_analysis/provinces/jiangsu.vue')
                    },
                    {
                        path:'/jiangxi',
                        name:'jiangxi',
                        component:()=>import(/*webpackChunkName:'jiangxi'*/ '@/page/data_analysis/provinces/jiangxi.vue')
                    },
                    {
                        path:'/jilin',
                        name:'jilin',
                        component:()=>import(/*webpackChunkName:'jilin'*/ '@/page/data_analysis/provinces/jilin.vue')
                    },
                    {
                        path:'/liaoning',
                        name:'liaoning',
                        component:()=>import(/*webpackChunkName:'liaoning'*/ '@/page/data_analysis/provinces/liaoning.vue')
                    },
                    {
                        path:'/neimenggu',
                        name:'neimenggu',
                        component:()=>import(/*webpackChunkName:'neimenggu'*/ '@/page/data_analysis/provinces/neimenggu.vue')
                    },
                    {
                        path:'/ningxia',
                        name:'ningxia',
                        component:()=>import(/*webpackChunkName:'ningxia'*/ '@/page/data_analysis/provinces/ningxia.vue')
                    },
                    {
                        path:'/qinghai',
                        name:'qinghai',
                        component:()=>import(/*webpackChunkName:'qinghai'*/ '@/page/data_analysis/provinces/qinghai.vue')
                    },
                    {
                        path:'/shaanxi',
                        name:'shaanxi',
                        component:()=>import(/*webpackChunkName:'shaanxi'*/ '@/page/data_analysis/provinces/shaanxi.vue')
                    },
                    {
                        path:'/shandong',
                        name:'shandong',
                        component:()=>import(/*webpackChunkName:'shandong'*/ '@/page/data_analysis/provinces/shandong.vue')
                    },
                    {
                        path:'/shanghai',
                        name:'shanghai',
                        component:()=>import(/*webpackChunkName:'shanghai'*/ '@/page/data_analysis/provinces/shanghai.vue')
                    },
                    {
                        path:'/shanxi',
                        name:'shanxi',
                        component:()=>import(/*webpackChunkName:'shanxi'*/ '@/page/data_analysis/provinces/shanxi.vue')
                    },
                    {
                        path:'/sichuan',
                        name:'sichuan',
                        component:()=>import(/*webpackChunkName:'sichuan'*/ '@/page/data_analysis/provinces/sichuan.vue')
                    },
                    {
                        path:'/tianjin',
                        name:'tianjin',
                        component:()=>import(/*webpackChunkName:'tianjin'*/ '@/page/data_analysis/provinces/tianjin.vue')
                    },
                    {
                        path:'/xinjiang',
                        name:'xinjiang',
                        component:()=>import(/*webpackChunkName:'xinjiang'*/ '@/page/data_analysis/provinces/xinjiang.vue')
                    },
                    {
                        path:'/xizang',
                        name:'xizang',
                        component:()=>import(/*webpackChunkName:'xizang'*/ '@/page/data_analysis/provinces/xizang.vue')
                    },
                    {
                        path:'/yunnan',
                        name:'yunnan',
                        component:()=>import(/*webpackChunkName:'yunnan'*/ '@/page/data_analysis/provinces/yunnan.vue')
                    },
                    {
                        path:'/zhejiang',
                        name:'zhejiang',
                        component:()=>import(/*webpackChunkName:'zhejiang'*/ '@/page/data_analysis/provinces/zhejiang.vue')
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
  // history: createWebHistory(process.env.BASE_URL),
    history: createWebHashHistory(),
    routes
})

export default router
