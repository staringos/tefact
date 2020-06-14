<template>
  <ArrPanel class="app-option-details" title="应用详情" border>
    <div class="app-details-container" v-if="currentApp">
      <AppDetails :app="currentApp" :onChange="(value) => handleDataChanged(null, value)" />
      <MenuList :menus="currentApp.menus" :pages="currentApp.pages" :onChange="(value) => handleDataChanged('menus', value)" />
      <PageList :pages="currentApp.pages" :entities="currentApp.entities" :onChange="(value) => handleDataChanged('pages', value)" />
    </div>
  </ArrPanel>
</template>
<style lang="scss">
  .app-details-container {
    padding-bottom: 50px;

    .code {
      background: #1b1b1b;
      color: wheat;
      overflow: auto;
      max-height: 500px;
    }

    .float-button {
      position: fixed;
      right: 50px;
      bottom: 200px;
      box-shadow: 0 0 7px 4px rgba(0, 0, 0, 0.12);
      z-index: 999;
    }
    .app-base-details {
      display: flex;
      flex: 1;

      .title-part {
        display: flex;
        flex-direction: column;
        flex: 1;
        justify-content: center;
        align-items: center;
      }
    }

    display: flex;
    flex: 1;
    flex-direction: column;
  }
</style>
<script lang="ts">
  import { Vue, Component, namespace, Watch } from 'nuxt-property-decorator'
  import { Application } from '~/services/common'

  import EntityList from '~/components/app/light/EntityList.vue'
  import MenuList from '~/components/app/light/MenuList.vue'
  import PageList from '~/components/app/light/PageList.vue'
  import AppDetails from '~/components/app/light/AppDetails.vue'

  const platform = namespace('platform')

  @Component({
    layout: 'plugin',
    components: {
      AppDetails, EntityList, MenuList, PageList
    }
  })
  export default class AppDetailsPage extends Vue {
    apps: Application[] = []
    currentApp: Application | null = null
    saveDialogVisible = false
    @platform.Getter appsGetter
    @platform.Action getPlatformConfig
    @platform.Action savePlatformConfig
    @platform.Action reConfigAndRestart

    async handleRestartTheServer() {
      const res = await this.reConfigAndRestart()
      if (res.status === 200) {
        this.$message({ message: '重启成功 正在刷新页面...', type: 'success' })
        location.reload()
      }
    }

    async handleSave() {
      const res = await this.savePlatformConfig({ key: this.currentApp?.key, config: this.currentApp })

      if (res.status === 200) {
        this.$message({ message: '操作成功', type: 'success' })
        return this.handleClose()
      }

      this.$message({ message: '操作失败', type: 'error' })
    }

    handleClose() {
      this.saveDialogVisible = false
    }

    handleSaveOpen() {
      this.saveDialogVisible = true
    }

    refreshCurrentApp() {
      const params = this.$route.params
      const find = this.apps && this.apps.filter(app => app.key === params.key)
      this.currentApp = find ? find[0] : null
    }

    @Watch('appsGetter')
    onAppsGetterChanged() {
      this.refreshApps()
    }

    handleDataChanged(key, value) {
      if (key) {
        // @ts-ignore
        Vue.set(this.currentApp, key, value)
        return
      }

      this.currentApp = value
    }

    refreshApps() {
      if (this.appsGetter.length !== this.apps.length) {
        this.apps = JSON.parse(JSON.stringify(this.appsGetter))
        this.refreshCurrentApp()
      }
    }

    public async beforeMount() {
      if (!this.appsGetter || this.appsGetter.length < 1)
        await this.getPlatformConfig()

      this.refreshApps()
    }

    mounted() {
    }
  }
</script>
