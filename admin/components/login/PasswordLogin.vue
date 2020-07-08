<template>
  <el-form class="login-form" :model="loginForm" status-icon :rules="rules" ref="ruleForm">
    <el-form-item prop="username" label="用户名" label-width="60px">
      <el-input v-model="loginForm.phone" placeholder="请输入用户名或手机" type="username" auto-complete="off" />
    </el-form-item>
    <el-form-item prop="password" label="密 码" label-width="60px">
      <el-input v-model="loginForm.password" placeholder="请输入密码" type="password" auto-complete="off" />
    </el-form-item>
    <el-form-item prop="code" label="验证码" label-width="60px">
      <el-col :span="13">
        <el-input v-model="loginForm.verify_code" placeholder="请输入验证码" type="text" auto-complete="off" class="passwordInput" />
      </el-col>
      <el-col :span="9" :offset="1">
        <img @click="refreshCode" :src="verifyImageUrl" class="verify-image"/>
      </el-col>
    </el-form-item>
    <el-button type="primary" @click="handleLogin('ruleForm')" class="login-btn">登 录</el-button>
  </el-form>
</template>
<script lang="ts">
  import { Component, namespace, Vue } from 'nuxt-property-decorator'
  import { LoginEntity } from '~/services/common'
  import Tools from '~/utils'

  const user = namespace('user')

  @Component
  export default class PasswordLogin extends Vue {
    loginForm: LoginEntity = {} as LoginEntity
    verifyImageUrl = ''
    uuid = ''

    rules = {
      phone: [{
        validator: (rule: any, value: any, callback: Function) => (value === ''  ? callback(new Error ('请输入用户名')) : ''),
        trigger: 'blur'
      }],
      password: [{
        validator: (rule: any, value: any, callback: Function) => (value === ''  ? callback(new Error ('请输入密码')) : ''),
        trigger: 'blur'
      }],
      verify_code: [{
        validator: (rule: any, value: any, callback: Function) => (value === ''  ? callback(new Error ('请输入验证码')) : ''),
        trigger: 'blur'
      }]
    }

    @user.Action verifyCode
    @user.Action passwordLogin

    async refreshCode() {
      const res = await this.verifyCode()
      const data = res.data.data
      this.verifyImageUrl = 'data:image/png;base64,' + data.verify_code_image
      this.uuid = data.uuid
    }

    async mounted() {
      this.refreshCode()
    }

    async handleLogin() {
      Tools.loginStatus(this, this.passwordLogin, {
        ...this.loginForm,
        uuid: this.uuid,
      })
    }
  }
</script>
<style lang="scss">
  .verify-image {
    width: 80px;
    height: 40px;
  }

  .login-btn {
    width: 100%;
    margin: 0 auto;
    border-radius: 15px;
  }
</style>
