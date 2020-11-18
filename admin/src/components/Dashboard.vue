<template>
  <div class="app-list">
    <div class="app-item" v-for="(app, i) in orgApps" :key="i" @click="() => handleAppClick(app)">
      <div class="app-item-bg"></div>
      <img class="icon" :src="app.icon + '?imageView2/0/w/200/h/200'"/>
      <div class="name">
        {{app.title}}
      </div>
    </div>

    <div class="app-item">
      <div class="app-item-bg"></div>
      <el-dropdown style="z-index: 999;" @command="handleCommand">
        <div class="icon">
          <i class="el-icon-plus"></i>
        </div>
        <div class="name">
          添加应用
        </div>

        <el-dropdown-menu slot="dropdown">
          <el-dropdown-item command="shop">应用商店</el-dropdown-item>
          <el-dropdown-item command="light" divided>轻应用</el-dropdown-item>
          <el-dropdown-item command="third" disabled>第三方应用</el-dropdown-item>
        </el-dropdown-menu>
      </el-dropdown>
    </div>
  </div>
</template>
<script>
  import { Component, Vue, namespace } from 'nuxt-property-decorator'
  import { DIALOG_NAME } from '~/store/system'
  import tools from '~/utils'

  const app = namespace('app')
  const system = namespace('system')

  @Component
  export default class Dashboard extends Vue {
    @app.Getter orgApps
    @app.Action setCurrentAppId
    @system.Action setDialogVisible

    handleAppClick(item) {
      tools.gotoAppIndex(item, this.$router)
    }

    handleCommand(command) {
      switch(command) {
        case 'shop':
          this.$router.push('/plugins/org/app')
          break
        case 'light':
          this.setDialogVisible({ key: DIALOG_NAME.LIGHT_APP_MODIFY_DIALOG, visible: true })
          break
        case 'third':
          this.$message({ message: '敬请期待' })
          break
        default:
          break
      }
    }
  }
</script>
<style lang="scss" scoped>
  @import "../assets/styles/variables";

  .app-list {
    display: flex;
    overflow: hidden;
    width: 100%;
    flex-wrap: wrap;
    justify-content: center;
    align-items: center;

    .app-item {
      align-items: center;
      display: flex;
      flex-direction: column;
      margin-right: 50px;
      margin-bottom: 30px;
      cursor: pointer;
      padding: 10px;
      position: relative;

      .el-icon-plus {
        font-size: 32px;
        margin: 0 auto;
        text-align: center;
        color: #1f69c0 !important;
        font-weight: bold;
      }

      .app-item-bg {
        display: none;
        background: white;
        border-radius: 20px;
        opacity: 0.6;
        position: absolute;
        top: 0;
        bottom: 0;
        left: 0;
        right: 0;
        z-index: 1;
      }

      &:hover {
        .app-item-bg {
          display: block;
        }
      }

      .icon {
        width: 100px;
        height: 100px;
        border-radius: 10px;
        background: #FFF;
        display: flex;
        align-items: center;
        text-align: center;
        z-index: 2;

        i {
          flex: 1;
          font-size: 36px;
          width: 50px;
          height: 50px;
          color: white;
          line-height: 50px;
        }
      }

      .name {
        color: $mainTextColor;
        margin-top: 10px;
        font-size: 20px;
        text-align: center;
        z-index: 2;
      }
    }
  }
</style>
