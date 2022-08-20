<template>
  <div>
<!--    顶部-->
    <div class="sidebar-top">
      <div>停车场后台管理</div>
      <div>
        <el-icon><SwitchButton /></el-icon>
      </div>
    </div>
    <el-divider />
    <div class="sidebar-cont">
      <el-menu :default-active="ac_index" @select="Select">
        <div v-for="(item,index) in menu" :key="index">
          <router-link :to="{path:item.router}">
            <el-menu-item v-if="item.Subclass.length == 0" :index="item.id">
              <el-icon>
                <component :is="item.icon"></component>
              </el-icon>
              <span>{{item.title}}</span>
            </el-menu-item>
          </router-link>
          <el-sub-menu v-if="item.Subclass.length > 0" :index="item.id">
            <template #title>
              <el-icon>
                <component :is="item.icon"></component>
              </el-icon>
              <span>{{item.title}}</span>
            </template>
            <div v-for="(two, index_two) in item.Subclass" :key="index_two">
              <router-link :to="{path:two.router}">
              <el-menu-item :index="two.id">{{two.title}}</el-menu-item>
              </router-link>
            </div>
          </el-sub-menu>

        </div>
      </el-menu>
    </div>
    <el-divider />

    <div class="sidebar-bottom">
      <div>
        <el-icon><Sunny /></el-icon>
        <p>&nbsp&nbsp复兴号动车组 FUXING EMU</p>
      </div>
    </div>
    <router-view></router-view>
  </div>
</template>

<script>
import {shallowRef,ref,onMounted} from 'vue'

import {
    DataAnalysis,
    Van,
    Camera,
    Sunny
} from '@element-plus/icons-vue'

export default {
    components:{DataAnalysis,Van,Camera},
    setup(){

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
                        router:'province_analysis',
                    },
                    {
                        id:'1-2',
                        title:'车型分析',
                        router:'model_analysis',
                    },
                    {
                        id:'1-3',
                        title:'时长分析',
                        router:'time_analysis',
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
                        router:'current_vehicle',
                    },
                    {
                        id:'2-2',
                        title:'出入记录',
                        router:'in_out_records',
                    }
                ]//是否有二级三级等等菜单
            },
            {
                id:'3',
                icon:Camera,
                title:'车牌识别',
                router:'lpdr',
                Subclass:[]//是否有二级三级等等菜单
            }
        ]

        const menu = shallowRef(Array)
        // 菜单激活回调
        const ac_index = ref('2-1')
        function Select(index,path){
            localStorage.setItem('menuid',JSON.stringify(index))
            localStorage.setItem('menupath',JSON.stringify(path))
        }
        onMounted(()=>{
            ac_index.value = JSON.parse(localStorage.getItem('menuid'))

            console.log(localStorage.getItem('menupath'))
        })

        return{menu,ac_index,Select}
    }
}




</script>

<style scoped>

</style>