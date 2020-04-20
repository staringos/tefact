<template>
  <div class="header-profile" v-if="currentUser">
    <img class="avatar" :src="currentUser.user_info.head_url" />
    <el-dropdown trigger="click" @command="handleClick">
      <div class="profile">
        <h2 class="username">{{currentUser.nickname}}</h2>
        <p class="job-title" v-if="currentOrg">{{currentOrg.staff_info.job_title}}</p>
        <i class="el-icon-arrow-down"></i>
      </div>

      <el-dropdown-menu slot="dropdown">
          <el-dropdown-item>您好，{{currentUser.nickname}}</el-dropdown-item>
          <el-dropdown-item command="details">个人资料</el-dropdown-item>
          <el-dropdown-item command="exit">退出登录</el-dropdown-item>
      </el-dropdown-menu>
    </el-dropdown>
  </div>
</template>
<script lang="ts">
  import { Component, Vue, namespace } from 'nuxt-property-decorator'

  const app = namespace('app')
  const user = namespace('user')
  const system = namespace('system')

  @Component({})
  export default class HeaderProfile extends Vue {
    @user.Getter currentUser
    @user.Action toggleUserDetailsDialog
    @app.Action getAllOrgs
    @app.Getter currentOrg
    @system.Action exit

    handleClick(command) {
      switch(command) {
        case 'details':
          this.toggleUserDetailsDialog(true)
          break
        case 'exit':
          this.exit()
          break
      }
    }

    mounted() {

    }
  }
</script>
<style lang="scss">
  .header-profile {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100%;

    .username {
      font-size: 16px;
      font-weight: 600;
    }

    .job-title {
      font-size: 12px;
    }
  }

  .profile {
    margin-right: 10px;
    padding-right: 15px;
    position: relative;

    .el-icon-arrow-down {
      float: right;
      position: absolute;
      right: 0;
      top: 0;
      height: 100%;
      display: flex;
      align-items: center;
    }
  }
  .avatar {
    width: 52px;
    height: 52px;
    border-radius: 50%;
    box-shadow:-1px 1px 6px 0px rgba(0,0,0,0.24);
    margin-left: 10px;
    margin-right: 10px;
    display: block;
  }
</style>
