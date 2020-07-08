<template>
  <div class="login-page">
    <img class="background-image" src="/bg6.jpg" />
    <div class="logo-area">
      <Logo />
    </div>
    <div class="login-page-container">
      <Card class="login-block">
        <el-row class="login-block-row">
          <el-col :span="12" class="login-block-item login-block-image">
            <img src="../../assets/images/login.png" />
          </el-col>
          <el-col :span="12" class="login-block-item login-block-form">
            <h1 class="title" v-if="loginType === 'login'">验证码登录</h1>
            <h1 class="title" v-else-if="loginType === 'Wechat'">微信登录</h1>
            <h1 class="title" v-else>密码登录</h1>
            <h2 class="description">Build System Without Code</h2>
            <div v-if="loginType === 'login'" style="width: 60%;margin: 0 auto">
              <PhoneLogin />
            </div>
            <div v-else-if="loginType === 'Wechart'" id="qrcode"></div>
            <div v-else style="width: 60%;margin: 0 auto">
              <PasswordLogin />
            </div>
            <p class="login-type">
              <span style="float:left;" @click="handleChangeLoginType">{{ loginType === 'login' ? '密码登录' : '验证码登录' }}</span>
              <span style="float: right" @click="handleRegister">免费注册</span>
            </p>
          </el-col>
        </el-row>
      </Card>
    </div>
  </div>
</template>
<style lang="scss">
  .login-page {
    width: 100%;
    height: 100%;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    background-color: #3b8070;
    position: relative;

    .background-image {
      position: absolute;
      top:0;
      left: 0;
      right: 0;
      bottom: 0;
      z-index: 1;
      width: 100%;
      min-height: 100%;
    }

    .logo-area {
      padding-top: 20px;
      justify-content: flex-start;
      display: flex;
      z-index:2;
    }

    .login-page-container {
      width: 100%;
      justify-content: center;
      align-items: center;
      display: flex;
      flex-grow: 1;
      z-index:2;

      .login-block {
        width: 80%;
        height: 450px;
        max-width: 800px;
        box-shadow:0px 6px 20px 2px rgba(201,226,252,0.5);

        .login-block-row {
          height: 100%;
        }

        .login-block-item {
          height: 100%;
          display: flex;
          justify-content: center;
          align-items: center;
        }

        #qrcode {
          height: 200px;
          text-align: center;
          margin: 0 auto;
          width: 50%;
          background: red;
        }

        .title {
          font-size: 46px;
          width: 80%;
          font-weight: 400;
        }

        .description {
          margin-bottom: 30px;
          width: 80%;
          font-weight: 300;
        }

        .login-block-form {
          background-color: white;
          flex-direction: column;

          .login-type {
            overflow: hidden;
            font-size: 14px;
            color: #909399;
            height: 20px;
            font-weight: 400;
            line-height: 20px;
            text-align: left;
            width: 60%;
            margin-top: 20px;
            cursor: pointer;
          }
        }
      }
    }
  }
</style>
<script lang="ts">
  import { Component, Vue, namespace, Watch } from 'nuxt-property-decorator'
  import Card from '~/components/ui/Card.vue'
  import Logo from '~/components/layout/UserAdmin/Logo.vue'
  import PhoneLogin from '~/components/login/PhoneLogin.vue'
  import PasswordLogin from '~/components/login/PasswordLogin.vue'

  @Component({
    components: { Card, PhoneLogin, PasswordLogin, Logo },
    layout: 'front'
  })
  export default class Index extends Vue {
    loginType = 'password'
    private mounted(): void {}

    @Watch('loginType')
    onLoginTypeChange() {
      if(this.loginType === 'Wechat') {
        this.requestWechatQRCode()
      }
    }

    public handleRegister() {
      this.$router.push("/register")
    }

    public requestWechatQRCode () {
        const ba64Css = 'LmltcG93ZXJCb3ggLnFyY29kZSB7d2lkdGg6IDE4MHB4O21hcmlnbi10b3A6LThweH0KLmltcG93ZXJCb3ggLnRpdGxlIHtkaXNwbGF5OiBub25lO30KLmltcG93ZXJCb3ggLmluZm8ge2Rpc3BsYXk6IG5vbmU7fQ=='
        const appid = 'wxa692729034d99a33'
        new (window as any).WxLogin({
            id: 'qrcode',
            appid: appid,
            scope: 'snsapi_login',
            redirect_uri: '',
            href: 'data:text/css;base64,' + ba64Css
        })
        document.getElementsByTagName('iframe')[0].style.height = '200px'
    }
    public handleChangeLoginType() {
      this.loginType = this.loginType === 'login' ? 'Wechat' : 'login'
    }
  }
</script>
