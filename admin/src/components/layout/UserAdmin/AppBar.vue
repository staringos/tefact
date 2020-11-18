<template>
  <div class="app-bar">
    <div class="expand-btn" @click="handleToggleMenu">
      <img src="../../../assets/images/icon/menu.svg" class="expand-btn-icon" />
    </div>
    <div class="app-list">
      <el-tooltip class="item" effect="dark" :content="app.title" placement="right" v-for="(app, i) in orgApps" :key="i">
        <a href="javascript:void(0);" @click="handleAppClick(app)">
          <div :class="`app-btn ${currentApp && currentApp.name === app.name ? ' active' : ''}`">
            <img :src="app.icon" />
          </div>
        </a>
      </el-tooltip>

      <el-tooltip class="item" effect="dark" content="添加应用" placement="right">
        <nuxt-link to="/">
          <div class="app-btn app-add-btn">
            <i class="el-icon-plus"></i>
          </div>
        </nuxt-link>
      </el-tooltip>
    </div>
    <el-tooltip class="bottom-btn" effect="dark" content="应用商店" placement="right-end">
      <i class="el-icon-s-goods" @click="toAppCenter"></i>
    </el-tooltip>
  </div>
</template>
<style lang="scss" scoped>
  @import "../../../assets/styles/variables";
  .app-bar {
    width: 62px;
    background: $mainColor;
    height: 100%;
    min-width: 62px;
    display: flex;
    flex-direction: column;

    .bottom-btn {
      width: 62px;
      height: 62px;
      display: flex;
      justify-content: center;
      align-items: center;

      &.el-icon-s-goods {
        font-size: 26px;
        color: #aed4f3;
        cursor: pointer;
      }
    }

    .app-list {
      display: flex;
      /*justify-content: center;*/
      align-items: center;
      flex-direction: column;
      flex-grow: 1;
      max-height: 100%;
      overflow-y: auto;

      .app-btn {
        width: 42px;
        height: 42px;
        border: 1px solid $borderSecondColor;
        border-radius: 10px;
        margin-top: 18px;
        background-color: #fff;
        opacity: 0.8;
        cursor: pointer;

        img {
          width: 100%;
          height: 100%;
        }

        &.active {
          opacity: 1;
        }

        &:hover {
          border-width: 2px;
        }
      }

      .app-add-btn {
        display: flex;
        justify-content: center;
        align-items: center;
        border-style: dashed;
        background-color: transparent;
        color: #fff;
        opacity: 1;
      }
    }

    .expand-btn {
      width: 100%;
      height: 62px;
      display: flex;
      justify-content: center;
      align-items: center;
      cursor: pointer;

      .expand-btn-icon {
        width: 24px;
        height: 24px;
      }
    }
  }
</style>
<script lang="ts">
  import { Component, Vue, namespace } from 'nuxt-property-decorator'
  import tools from '~/utils'

  const app = namespace('app')
  const system = namespace('system')

  @Component({})
  export default class AppBar extends Vue {
    @app.Getter orgApps
    @app.Getter currentApp
    @system.Action togglePluginMenu
    @app.Action setCurrentAppId

    toAppCenter() {
      this.$router.push('/plugins/org/app')
    }

    handleAppClick(app) {
      if (this.currentApp && this.currentApp.id === app.id) return

      tools.gotoAppIndex(app, this.$router)
    }

    handleToggleMenu() {
      this.togglePluginMenu()
    }
  }
</script>
