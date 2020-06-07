<template>
  <div class="menu-bar">
    <div class="expand-btn" @click="handleToggleMenu">
      <img src="../../assets/images/icon/menu.svg" class="expand-btn-icon" />
    </div>
    <div class="menu-list">
      <el-tooltip class="item" effect="dark" :content="menu.title" placement="right" v-for="(menu, i) in menus" :key="i">
        <a :class="`menu-item ${active === menu.id ? 'active' : ''}`" href="javascript:void(0);" @click="handleMenuClick(menu)">
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

      .menu-item {
        text-decoration: none;

        &.active, &:hover {
          .editor-menu-btn {
            box-sizing: border-box;
            border-left: 4px solid white;
          }
        }
      }

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
      { id: "home", icon: "tf-icon-all", title: "基本信息", route: "/app/light/${id}/" },
      { id: "menu-page", icon: "tf-icon-integral", title: "菜单页面", route: "/app/light/${id}/menu-page" },
      { id: "data-source", icon: "tf-icon-packing-labeling", title: "数据源", route: "/app/light/${id}/data-source" },
      { id: "setting", icon: "tf-icon-conditions", title: "应用设置", route: "/app/light/${id}/setting" }
    ]

    handleMenuClick(menu) {
      this.$router.push(menu.route.replace("${id}", this.id))
    }

    get id () {
      return this.$route.params.id;
    }

   handleToggleMenu() {
      this.togglePluginMenu()
    }

    get active() {
      const route = this.$route.path

      if (route.indexOf("menu-page") > -1) {
        return "menu-page"
      }

      if (route.indexOf("data-source") > -1) {
        return "data-source"
      }

      if (route.indexOf("setting") > -1) {
        return "setting"
      }

      return "home"
    }
  }
</script>
