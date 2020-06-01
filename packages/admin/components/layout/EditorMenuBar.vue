<template>
  <div class="menu-bar">
    <div class="expand-btn" @click="handleToggleMenu">
      <img src="../../assets/images/icon/menu.svg" class="expand-btn-icon" />
    </div>
    <div class="menu-list">
      <el-tooltip class="item" effect="dark" :content="menu.title" placement="right" v-for="(menu, i) in menus" :key="i">
        <a href="javascript:void(0);" @click="handleMenuClick(menu)">
          <div :class="`editor-menu-btn ${currentMenu && currentMenu === menu.route ? ' active' : ''}`">
            <i :class="`tefact-icon ${menu.icon}`"></i>
            <span class="menu-btn-title">{{menu.title}}</span>
          </div>
        </a>
      </el-tooltip>

      <el-tooltip class="item" effect="dark" content="添加应用" placement="right">
        <nuxt-link to="/">
          <div class="menu-btn menu-add-btn">
            <i class="el-icon-plus"></i>
          </div>
        </nuxt-link>
      </el-tooltip>
    </div>
  </div>
</template>
<style lang="scss" scoped>
  @import "../../assets/styles/variables";
  .menu-bar {
    width: 70px;
    background: $editor-menu-color;
    height: 100%;
    min-width: 70px;
    display: flex;
    flex-direction: column;

    .bottom-btn {
      width: 70px;
      height: 70px;
      display: flex;
      justify-content: center;
      align-items: center;

      &.el-icon-s-goods {
        font-size: 26px;
        color: #aed4f3;
        cursor: pointer;
      }
    }

    .menu-list {
      display: flex;
      align-items: center;
      flex-direction: column;
      flex-grow: 1;

      .editor-menu-btn {
        width: 70px;
        height: 70px;
        cursor: pointer;
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
        color: white;


        .tefact-icon {
          font-size: 28px;
          color: white;
        }

        .menu-btn-title {
          font-size: 12px;
          color: white;
        }

        &.active, &:hover {
          border-left: 3px solid white;
        }
      }

      .menu-add-btn {
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
  import tools from '@arrplat/utils'

  const menu = namespace('menu')
  const system = namespace('system')

  @Component({})
  export default class menuBar extends Vue {
    @system.Action togglePluginMenu

    currentMenu = "/"

    menus = [
      { icon: "tf-icon-all", title: "基本信息", route: "/" },
      { icon: "tf-icon-integral", title: "菜单页面", route: "/menu-page" },
      { icon: "tf-icon-packing-labeling", title: "数据源", route: "/data-source" },
      { icon: "tf-icon-conditions", title: "应用设置", route: "/setting" }
    ]

    handleMenuClick(menu) {
    }

    handleToggleMenu() {
      this.togglePluginMenu()
    }
  }
</script>
