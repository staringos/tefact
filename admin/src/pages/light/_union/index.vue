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
            <el-button type="text" class="button" @click.stop="handleEdit(item)">分享</el-button>
          </div>
        </div>
      </el-card>
    </div>
  </ArrPanel>
</template>
<style lang="scss">

</style>
<script lang="ts">
  import { Vue, Component, namespace, Watch } from 'nuxt-property-decorator'
  import { Application } from "~/services/common/entities/app"

  const app = namespace('app')

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
    layout: 'plugin'
  })
  export default class HomePage extends Vue {
    @app.Getter currentApp
    @app.Action getAppDetails

    activeName: string = 'all'
    list: ListItem[] = []
    app!: Application

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
