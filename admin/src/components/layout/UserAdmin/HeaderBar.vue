<template>
  <el-menu :default-active="activeIndex" router class="header-bar" mode="horizontal">
    <Logo :title="title" color="#303133" :direct="direct" />
    <div class="header-bar-main">
      <el-menu-item :index="getWorkspaceIndex()">工作台</el-menu-item>
      <el-menu-item index="/admin">桌面</el-menu-item>
    </div>
    <div class="header-right" v-if="checkLoginStatus">
      <Toolbar />
      <HeaderProfile />
    </div>
    <div class="header-right" v-if="!checkLoginStatus">
      <el-button type="text" size="small" @click="handleLogin">登录</el-button>
      <div class="btn-wrapper">
        <el-button type="primary" size="small" @click="handleRegister">免费注册</el-button>
      </div>
    </div>
    <CreateOrgDialog />
    <UserDetailDialog />
    <UserModifyDialog />
    <NoOrgDialog />
    <BasicModifyDialog />
  </el-menu>
</template>
<script lang="ts">
  import Logo from './Logo.vue'
  import CreateOrgDialog from '../../organization/CreateOrgDialog.vue'
  import { Component, Vue, namespace, Prop } from 'nuxt-property-decorator'
  import HeaderProfile from '~/components/layout/HeaderProfile.vue'
  import Toolbar from '~/components/layout/Toolbar.vue'
  import UserDetailDialog from '~/components/user/UserDetailDialog.vue'
  import UserModifyDialog from '~/components/user/UserModifyDialog.vue'
  import NoOrgDialog from '~/components/organization/NoOrgDialog.vue'
  import BasicModifyDialog from '~/components/app/BasicModifyDialog.vue'

  const app = namespace('app')
  const user = namespace('user')

  @Component({
    components: {
      BasicModifyDialog,
      UserDetailDialog,
      Toolbar,
      HeaderProfile,
      Logo,
      CreateOrgDialog,
      UserModifyDialog,
      NoOrgDialog
    }
  })
  export default class HeaderBar extends Vue {
    props = {}
    activeIndex = '0'

    @app.Getter orgApps
    @user.Getter checkLoginStatus
    @Prop(String) title!: string | null
    @Prop({ default: '/' }) direct

    handleLogin() {
      this.$router.push({path: '/auth'})
    }

    handleRegister() {
      this.$router.push({path: '/auth?type=register'})
    }

    getWorkspaceIndex() {
      const { orgApps } = this
      if (!orgApps) return "/admin"
      const cur = orgApps[0]
      if (!cur) return "/admin"

      switch(cur.type) {
        case "light":
          return `/light/${cur.admin_route}`
        default:
          return `/plugins/${cur.admin_route}`
      }
    }
  }
</script>
<style lang="scss">
  @import "../../../assets/styles/variables";

  .header-bar {
    display: flex;
    height: 62px;
    min-height: 62px;
    justify-content: space-between;
    outline:0;

    div {
      &:focus {
        outline:0 !important;
      }
    }

    .el-menu-item, .el-menu--horizontal > .el-menu-item {
      height: 62px;
    }

    .header-bar-main {
      display: flex;
      margin: 0 auto;
      height: 100%;
    }

    .show-menu-btn {
      float: left;
      align-items: center;
      display: flex;
    }

    .header-right {
      margin-right: 20px;
      display: flex;
      .btn-wrapper {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-left: 18px;
      }
      /*margin-left: auto;*/
    }
  }
</style>
