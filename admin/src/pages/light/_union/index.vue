<template>
  <ArrPanel class="home-page" v-if="currentApp" :title="currentApp.title" border>
    <el-tabs v-model="activeName" @tab-click="handleClick">
      <el-tab-pane label="全部" name="all"></el-tab-pane>
      <el-tab-pane label="PC页" name="pc"></el-tab-pane>
      <el-tab-pane label="H5" name="h5"></el-tab-pane>
      <el-tab-pane label="表单" name="form"></el-tab-pane>
    </el-tabs>
    <div class="home-page-content">
      <el-card class="app-item-card" v-for="(item, key) in list" :key="key" :body-style="{ padding: '0px' }" @click.native="handleTo(item)">
        <img v-if="!item.image" :src="item.image" class="image">
        <i else class="tefact-icon tf-icon-pages"></i>
        <div style="padding: 14px;">
          <span>{{ item.name }}</span>
          <div class="bottom clearfix">
            <el-button type="text" class="button" @click.stop="handleEdit(item)">编辑</el-button>
            <el-button type="text" class="button" @click.stop="handlePreviewer(item)">预览</el-button>
          </div>
        </div>
      </el-card>
      <el-card class="app-item-card add-page" body-style="{ padding: '0px' }" @click.native="handleOpenModify">
        <i class="el-icon-plus"></i>
      </el-card>
    </div>
    <PageModifyDialog v-if="currentApp" :isEdit="isEdit" :form="form" :dialogVisible="showAddPage" :appId="currentApp.id" @cancel="handleCancel" @refresh="refresh" />
    <Previewer :page="page" :show="showPreviewer" @cancel="handlePreviewerHide" />
  </ArrPanel>
</template>
<style lang="scss" scoped>
  .home-page-content {
    .add-page {
      display: flex;
      justify-content: center;
      align-items: center;

      .el-icon-plus {
        font-size: 52px;
      }
    }
  }
</style>
<script lang="ts">
  import { Vue, Component, namespace, Watch } from 'nuxt-property-decorator'
  import { Application } from "~/services/common/entities/app"
  import PageModifyDialog from "~/components/app/light/page/PageModifyDialog.vue"
  import Previewer from "~/components/app/light/page/Previewer.vue"
  import Constants from "~/services/common/constants"
  import cloneDeep from 'lodash/cloneDeep'

  const app = namespace('app')
  const editor = namespace('editor')

  type ListItemType = 'page' | 'form'

  type ListItem = {
    id?: string,
    name?: string,
    image?: string | null,
    link?: string,
    icon?: string,
    type?: ListItemType
  }

  @Component({
    components: {Previewer, PageModifyDialog},
    layout: 'plugin'
  })
  export default class HomePage extends Vue {
    @app.Getter currentApp
    @app.Action getAppDetails
    @editor.Action getPageDetails

    activeName: string = 'all'
    page = null
    form = cloneDeep(Constants.entities.DefaultPage)
    list: ListItem[] = []
    app!: Application
    showPreviewer: Boolean = false
    showAddPage: Boolean = false
    isEdit: Boolean = false

    handlePreviewerHide() {
      this.showPreviewer = false
      this.page = null
    }

    handleOpenModify() {
      this.showAddPage = true
    }

    handleCancel() {
      this.showAddPage = false
      this.isEdit = false
      this.form = cloneDeep(Constants.entities.DefaultPage)
    }

    @Watch('activeName', { immediate: true })
    handleSwitchActive() {
      if (!this.app) return
      const res = [] as ListItem[]

      switch (this.activeName) {
        case "all":
          this.app.pages.forEach(page => {
            res.push({
              id: page.id,
              name: page.title,
              image: page.head_image,
              link: "",
              type: "page",
              icon: ""
            })
          })
      }

      this.list = res;
    }

    handleTo(page) {
      this.$router.push(`/app/light/page/${page.id}`)
    }

    handleEdit(page) {
      this.$router.push(`/app/light/${this.currentApp.id}/${page.id}/editor`)
    }

    handleClick(e) {
      this.activeName = e
    }

    async handlePreviewer(item) {
      this.page = await this.getPageDetails(item.id)
      this.showPreviewer = true
    }

    async refresh() {
      if (!this.currentApp) return
      const res = await this.getAppDetails(this.currentApp.id)
      this.app = res.data.data
      this.handleSwitchActive()
    }

    @Watch("currentApp")
    handleCurrentAppChange() {
      this.refresh()
    }

    mounted() {
      this.refresh()
    }
  }
</script>
<style lang="scss" scoped>
.home-page {
  ::v-deep .panel-content {
    flex-direction: column;
  }

  .home-page-content {
    flex: 1;
    min-height: 100%;
    flex-direction: row;
    display: flex;
    flex-wrap: wrap;
  }

  .app-item-card {
    width: 235px;
    margin: 10px 1.5%;
    height: 347px;

    &:hover {
      border: 1px solid $thirdColor;
    }

    image {
      height: 235px;
    }

    .tf-icon-pages {
      height: 235px;
      display: flex;
      justify-content: center;
      align-items: center;
      font-size: 200px;
      color: $thirdColor;
    }
  }
}
</style>
