<template>
  <ArrPanel title="应用中心" border>
    <div class="app-list">
      <AppItem :item="item" :key="i" v-for="(item, i) in allAppsGetter" @onClick="handleItemClick"></AppItem>
    </div>
    <el-dialog
      title="应用详情"
      :visible.sync="detailDialogVisible"
      width="40%"
      :before-close="handleDialogClose">
      <AppItemDetails v-if="detailDialogVisible" :item="currentApp" @onDismiss="handleDialogClose" />
    </el-dialog>
  </ArrPanel>
</template>
<style lang="scss" scoped>
  .app-list {
    display: flex;
    flex: 1;
    flex-wrap: wrap;
  }
</style>
<script lang="ts">
  import { Component, Vue, namespace } from 'nuxt-property-decorator'
  import AppItem from '~/components/org/AppItem.vue'
  import AppItemDetails from '~/components/org/AppItemDetails.vue'
  import { Application } from '~/services/common/entities/app'

  const app = namespace('app')

  @Component({
    layout: 'plugin',
    components: {
      AppItem, AppItemDetails
    }
  })
  export default class Apps extends Vue {
    detailDialogVisible: boolean = false
    currentApp: Application = {} as Application

    @app.Getter currentOrg
    @app.Getter allAppsGetter
    @app.Action getAllApps

    handleItemClick(app) {
      this.detailDialogVisible = true
      this.currentApp = app
    }

    handleDialogClose() {
      this.detailDialogVisible = false
    }

    beforeMount() {
      this.getAllApps(this.currentOrg.id)
    }
  }
</script>
