<template>
  <div id="backcont">
    <div class="median-set">
      <div class="login-cont">
        <div class="login-cont-title">停车场管理平台</div>
        <div class="login-cont-user">
          <p>账号</p>
          <el-input v-model="account" class="inputflex" placeholder="请输入账号" clearable />
        </div>
        <div class="login-cont-user">
          <p>密码</p>
          <el-input v-model="password" class="inputflex" placeholder="请输入密码" clearable />
        </div>
        <!-- 登录和注册按钮的切换 -->
        <div class="reg-view" @click="regi = regi == '登录' ? '注册' : '登录'"><p>{{regi}}</p></div>
        <!--    登录或注册按钮提交    -->

        <el-button v-if="regi == '注册'" type="success" class="login-cont-button" @click="login">登录</el-button>
        <el-button v-else type="success" class="login-cont-button">注册</el-button>

      </div>
    </div>
  </div>
</template>

<script>
import {reactive, toRefs} from 'vue'
import {useRouter} from 'vue-router'
export default {
  setup(){

    const user = reactive({
      account:'',
      password:'',
      regi:'注册'
    })

    function login(){
      window.open(window.location.href + 'index', '_self')
    }

    return{...toRefs(user), login}
  }
}
</script>

<!--<script setup>-->
<!--import {reactive, toRefs} from "vue";-->

<!--const user = reactive({-->
<!--  account:'',-->
<!--  password:'',-->
<!--  regi:'注册'-->
<!--})-->
<!--const users = toRefs(user)-->

<!--</script>-->

<style scoped>

</style>