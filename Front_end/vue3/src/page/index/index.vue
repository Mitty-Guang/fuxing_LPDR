<template>
  <div>
<!--    顶部-->
    <div class="sidebar-top">
      <div>停车场后台管理</div>
      <div>退出</div>
    </div>
    <div class="sidebar-cont">
      <el-menu :default-active="ac_index" @select="Select">
        <div v-for="(item,index) in menu" :key="index">
          <el-menu-item v-if="item.Subclass.length == 0" :index="item.id">
            <el-icon>
              <component :is="item.icon"></component>
            </el-icon>
            <span>{{item.title}}</span>
          </el-menu-item>

          <el-sub-menu v-if="item.Subclass.length > 0" :index="item.id">
            <template #title>
              <el-icon>
                <component :is="item.icon"></component>
              </el-icon>
              <span>{{item.title}}</span>
            </template>
            <div v-for="(two, index_two) in item.Subclass" :key="index_two">
              <el-menu-item :index="two.id">{{two.title}}</el-menu-item>
            </div>
          </el-sub-menu>

        </div>
      </el-menu>
    </div>
    <router-view></router-view>
  </div>
</template>

<script>
import {shallowRef,ref,onMounted} from 'vue'
import {
    DataAnalysis,
    Van,
    Camera
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

        const menu = shallowRef(Array)
        // 菜单激活回调
        const ac_index = ref('1-1')
        function Select(index,path){
            localStorage.setItem('menuid',JSON.stringify(index))
        }
        onMounted(()=>{
            ac_index.value = JSON.parse(localStorage.getItem('menuid'))
        })

        return{menu,ac_index,Select}
    }
}




</script>

<style scoped>

</style>