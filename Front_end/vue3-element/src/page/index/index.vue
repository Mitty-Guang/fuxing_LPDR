<template>
  <div>
<!--    顶部-->
    <div class="sidebar-top">
      <div>停车场后台管理</div>
      <div>退出</div>
    </div>
    <div class="sidebar-cont">
      <el-menu>
        <el-sub-menu index="1">
          <template #title>
            <el-icon><DataAnalysis /></el-icon>
            <span>数据分析</span>
          </template>
          <el-menu-item index="1-1">省份分析</el-menu-item>
          <el-menu-item index="1-2">车型分析</el-menu-item>
          <el-menu-item index="1-3">时长分析</el-menu-item>
        </el-sub-menu>
        <el-sub-menu index="2">
          <template #title>
            <el-icon><Van /></el-icon>
            <span>车辆管理</span>
          </template>
          <el-menu-item index="2-1">当前车辆</el-menu-item>
          <el-menu-item index="2-2">出入记录</el-menu-item>
        </el-sub-menu>
        <el-menu-item index="3">
          <el-icon><Camera /></el-icon>
          <span>车牌识别</span>
        </el-menu-item>
      </el-menu>
    </div>
  </div>
</template>

<script setup>
import {
    DataAnalysis,
    Van,
    Camera
} from '@element-plus/icons-vue'
import {reactive} from 'vue'
const Array = [
    {
        id:'1',
        icon:DataAnalysis,
        title:'数据分析',
        router:'',
        Subclass:[
            {
                id:'1-1',
                title:'省份分析',
                router:'',
            },
            {
                id:'1-2',
                title:'车型分析',
                router:'',
            },
            {
                id:'1-3',
                title:'时长分析',
                router:'',
            }
        ]//是否有二级三级等等菜单
    },
    {
        id:'2',
        icon:Van,
        title:'车辆管理',
        router:'',
        Subclass:[
            {
                id:'2-1',
                title:'当前车辆',
                router:'',
            },
            {
                id:'2-2',
                title:'出入记录',
                router:'',
            }
        ]//是否有二级三级等等菜单
    },
    {
        id:'3',
        icon:Camera,
        title:'车牌识别',
        router:'',
        Subclass:[]//是否有二级三级等等菜单
    }
]




</script>

<style scoped>

</style>