<template>
  <div class="login-page">
    <Card class="login-block">
      <el-row class="login-block-row">
        <el-col :span="12" class="login-block-item login-block-image">
          <img src="../../assets/images/login.png" />
        </el-col>
        <el-col :span="12" class="login-block-item login-block-form">
          <h1 class="title">Arrplat</h1>
          <h2 class="description">企业统一中台解决方案</h2>
              <el-form class="login-form" :model="loginForm" status-icon :rules="rules" ref="ruleForm">
                <el-form-item prop="username">
                  <el-input v-model="loginForm.username" placeholder="手机号" type="username" auto-complete="off" />
                </el-form-item>
                <el-form-item prop="password">
                  <el-col :span="13">
                    <el-input v-model="loginForm.code" placeholder="验证码" type="text" auto-complete="off" class="passwordInput" />
                  </el-col>
                  <el-col :span="10" :offset="1">
                    <el-button type="primary" @click="verification">{{ msg }}</el-button>
                  </el-col>
                </el-form-item>
                <el-button type="primary" @click="handleLogin('ruleForm')" class="login-btn">提交</el-button>
              </el-form>
        </el-col>
      </el-row>
    </Card>
  </div>
</template>

<script lang="ts">
import { Vue, namespace, Component } from 'nuxt-property-decorator'
import Card from '~/components/ui/Card.vue'
import { LoginEntity } from '@arrplat/common'

const success = namespace('success')
@Component({
    components: { Card },
    layout: 'front'
})
export default class Success extends Vue {
  loginForm : LoginEntity = {} as LoginEntity
  rules = {
    username: [{
      validator: (rule: any, value: any, callback: Function) => (value === ''  ? callback(new Error ('请输入用户名')) : ''),
      trigger: 'blur'
    }],
    code: [{
      validator: (rule: any, value: any, callback: Function) => (value === ''  ? callback(new Error ('请输入密码')) : ''),
      trigger: 'blur'
    }]
  }
  msg = '获取验证码'
  public handleLogin() {}
  public verification() {}
}
</script>

<style scoped>

</style>
