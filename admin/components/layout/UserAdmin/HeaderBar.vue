<template>
  <el-menu :default-active="activeIndex" router class="header-bar" mode="horizontal">
    <Logo :title="title" color="#303133" />
    <div class="header-bar-main">
      <el-menu-item :index="`/plugins/${orgApps && orgApps[0] ? orgApps[0].admin_route : '' }`">工作台</el-menu-item>
      <el-menu-item index="/admin">桌面</el-menu-item>
    </div>
    <div class="header-right">
      <Toolbar />
      <HeaderProfile />
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
    @Prop(String) title!: string | null
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
      /*margin-left: auto;*/
    }
  }
</style>
