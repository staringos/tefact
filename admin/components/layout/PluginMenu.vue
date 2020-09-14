<template>
  <div class="plugin-menu" v-if="showPluginMenuGetter">
    <div class="plugin-menu-title">
      <img v-if="currentApp" :src="currentApp.icon" />
      <h3 v-if="currentApp">
        {{currentApp.title}}
      </h3>
      <el-button type="text" icon="el-icon-edit" @click.stop="handleToAppEditor" circle></el-button>
    </div>
    <div class="plugin-menu-wrapper">
      <el-menu
        default-active="2"
        class="plugin-menu-content"
        unique-opened
        v-if="currentApp"
        router
      >
        <template v-for="(menu, i) in currentApp.menus" >
          <el-menu-item v-if="!menu.children || menu.children.length < 1" :index="getPath(menu)">
            <i :class="menu.icon + 'menu-icon'" v-if="!menu.icon.startsWith('http')"></i>
            <img class="menu-icon" :src="menu.icon" v-if="menu.icon.startsWith('http')" />
            <span slot="title">{{menu.name}}</span>
          </el-menu-item>

          <el-submenu v-if="menu.children && menu.children.length > 0" :index="menu.id">
            <template slot="title">
              <i :class="menu.icon + 'menu-icon'" v-if="!menu.icon.startsWith('http')"></i>
              <img class="menu-icon" :src="menu.icon" v-if="menu.icon.startsWith('http')" />
              <span>{{menu.name}}</span>
            </template>
            <el-menu-item :index="getPath(child)" :key="i" v-for="(child, i) in menu.children">
              {{child.name}}
              <el-button class="page-edit-btn" type="text" icon="el-icon-edit" @click="handleToPageEditor(child.page_id)" circle></el-button>
            </el-menu-item>
          </el-submenu>
        </template>
      </el-menu>
    </div>
  </div>
</template>
<style lang="scss" scoped>
  @import '../../assets/styles/variables';

  .plugin-menu {
    display: flex;
    flex-direction: column;
    height: 100%;
    width: 200px;
    min-width: 200px;

    .page-edit-btn {
      float: right;
      padding: 0;
      line-height: 50px;

      ::v-deep .el-icon-edit {
        color: #0d5aa7;
        font-size: 14px;
      }
    }

    .plugin-menu-wrapper {
      flex: 1;
      display: flex;
    }

    .el-menu {
      box-sizing: border-box;
    }

    .plugin-menu-title {
      border-right: 1px solid $borderColor;
      border-bottom: 1px solid $borderColor;
      border-top: 0;
      height: 69px;
      line-height: 69px;
      display: flex;
      justify-content: center;
      align-items: center;
      box-sizing: border-box;

      h3 {
        line-height: 32px;
        padding-left: 10px;
        font-weight: normal;
      }

      img {
        width: 32px;
        height: 32px;
        display: inline-block;
      }
    }

    .plugin-menu-content {
      width: 100%;
      flex: 1;
      overflow: auto;

      .menu-icon {
        width: 30px;
        height: 30px;
      }
    }
  }
</style>
<script>
  import { Component, Vue, namespace } from 'nuxt-property-decorator'
  import { cloneDeep } from 'lodash-es'

  const app = namespace('app')
  const system = namespace('system')

  @Component({})
  export default class PluginMenu extends Vue {
    lodash = { cloneDeep }

    @app.Getter currentApp
    @system.Getter showPluginMenuGetter

    handleToAppEditor() {
      this.$router.push(`/app/light/${this.currentApp.id}`)
    }

    handleToPageEditor(pageId) {
      this.$router.push(`/app/light/${this.currentApp.id}/${pageId}/editor`)
    }

    getPath (menu) {
      console.log("menu:", menu);
      if (menu.type === 2 && menu.page_id) {
        return `/app/light/page/${menu.page_id}`
      }

      return _.startsWith(menu.link, 'http') || menu.link.startsWith('/') ? menu.link : `/plugins/${this.currentApp.admin_route}/${menu.link}`
    }
  }
</script>
