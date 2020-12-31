<template>
  <div class="app-wrapper">
    <AppBar />
    <el-row class="main">
      <HeaderBar />
      <div class="plugin-content" v-if="allOrgs && allOrgs.length > 0">
        <PluginMenu />
        <div class="main-container">
          <nuxt />
        </div>
      </div>
      <SettingBtn />
    </el-row>
  </div>
</template>
<style lang="scss">
  .plugin-content {
    display: flex;
    flex-direction: row;
    max-height: 100%;
    width: 100%;
    flex-grow: 1;
  }
</style>
<script lang="ts">
  import { Component, Vue, namespace } from 'nuxt-property-decorator'
  import HeaderBar from '../components/layout/UserAdmin/HeaderBar.vue'
  import AppBar from '../components/layout/UserAdmin/AppBar.vue'
  import PluginMenu from '~/components/layout/PluginMenu.vue'
  import SettingBtn from '~/components/layout/SettingBtn.vue'

  const app = namespace('app')

  @Component({
    components: {
      PluginMenu, HeaderBar, AppBar, SettingBtn
    }
  })
  export default class Plugin extends Vue {
    props = {}
    data () {
      return {}
    }

    @app.Action('init') init:any
    @app.Getter allOrgs

    created () {
      if (process.server) return
      this.init()
    }
  }
</script>
