<template>
  <el-form class="login-form" :model="form" status-icon :rules="rules" ref="form">
<!--    <el-form-item prop="username" label="手机号" label-width="70px">-->
<!--      <el-input v-model="form.phone" placeholder="请输入手机号" type="text" auto-complete="off" />-->
<!--    </el-form-item>-->
    <el-form-item prop="username" label="用户名" label-width="80px" required>
      <el-input v-model="form.username" placeholder="请输入用户名" type="text" auto-complete="off" />
    </el-form-item>
    <el-form-item prop="password" label="密码" label-width="80px" required>
      <el-input v-model="form.password" placeholder="请输入密码" type="password" auto-complete="off" />
    </el-form-item>
    <el-form-item prop="re_password" label="重复密码" label-width="80px" required>
      <el-input v-model="form.re_password" placeholder="请再次输入密码" type="password" auto-complete="off" />
    </el-form-item>
    <el-button type="primary" @click="handleRegister" class="login-btn">注册</el-button>
  </el-form>
</template>
<script lang="ts">
  import { Component, namespace, Vue } from 'nuxt-property-decorator'
  import { checkPhone } from '~/utils'
  import { RegisterParams } from "~/services/common/entities/user";

  const user = namespace('user')

  @Component
  export default class Index extends Vue {
    form: RegisterParams = {} as RegisterParams
    lock = true
    timeout: any = null
    rules = {
      username: [{
        validator: (rule: any, value: any, callback: Function) => (value === ''  ? callback(new Error ('请输入用户名')) : callback()),
        trigger: 'blur'
      }],
      password: [{
        validator: (rule: any, value: any, callback: Function) => {
          if (!value || value === '' || value.term === '') return callback(new Error ('请输入密码'))
          if (value.length < 8) return callback(new Error ('密码不能小于八位'))
          return callback()
        },
        trigger: 'blur'
      }],
      phone: [{
        validator: (rule: any, value: any, callback: Function) => (value && !checkPhone(value) ? callback(new Error ('请输入正确的手机号')) : callback()),
        trigger: 'blur'
      }],
      re_password: [{
        validator: (rule: any, value: any, callback: Function) => {
          console.log("value:", value, this.form.password)
          return (this.form.password !== value ? callback(new Error ('密码数据不一致')) : callback())
        },
        trigger: 'blur'
      }]
    }

    @user.Action register!: Function
    @user.Action verification:any

    public async handleRegister() {
      (this.$refs.form as HTMLFormElement).validate(valid => {
        if (!valid) return false;
        this.register(this.form).then(res => {
          this.$message({ message: "注册成功，请登录", type: 'success' })
          this.$router.push("/auth?type=password")
        }).catch(e => {
          console.log("e.data.message:", e.data.message)
          this.$message({ message: e.data.message, type: 'error' })
        })
        return false;
      })
    }
  }
</script>

<style lang="scss" scoped>
  .login-form {
    display: flex;
    flex-direction: column;
  }

  .login-btn {
    width: 100%;
    margin: 0 auto;
    border-radius: 15px;
  }
</style>
