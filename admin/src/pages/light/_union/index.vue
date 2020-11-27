<template>
  <ArrPanel class="home-page" v-if="currentApp" :title="currentApp.title" border>
    <p>首页</p>
    <el-tabs v-model="activeName" @tab-click="handleClick">
      <el-tab-pane label="all" name="fourth">全部</el-tab-pane>
      <el-tab-pane label="pc" name="first">PC页</el-tab-pane>
      <el-tab-pane label="h5" name="second">H5</el-tab-pane>
      <el-tab-pane label="form" name="third">表单</el-tab-pane>
    </el-tabs>
    <div class="home-page-content">
      <el-card :body-style="{ padding: '0px' }">
        <img src="https://shadow.elemecdn.com/app/element/hamburger.9cf7b091-55e9-11e9-a976-7f4d0b07eef6.png" class="image">
        <div style="padding: 14px;">
          <span>好吃的汉堡</span>
          <div class="bottom clearfix">
            <el-button type="text" class="button">修改</el-button>
            <el-button type="text" class="button">分享</el-button>
            <el-button type="text" class="button">删除</el-button>
          </div>
        </div>
      </el-card>
    </div>
  </ArrPanel>
</template>
<style lang="scss">

</style>
<script lang="ts">
  import { Vue, Component, namespace } from 'nuxt-property-decorator'

  const app = namespace('app')

  type List = {
    name: string,
    image: string,
    link: string,
    icon: string
  }

  @Component({
    layout: 'plugin'
  })
  export default class HomePage extends Vue {
    @app.Getter currentApp

    activeName: string = 'all'
    list!: List

    handleClick(e) {
      this.activeName = e
    }

    mounted() {
      console.log("this.current:", this.currentApp)
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
  }
}
</style>
