<template>
  <div class="app-menu">
    <div class="title-part">
      <el-avatar :size="50" :src="app.icon" />
      <h3>{{app.title}}</h3>
    </div>
    <el-menu default-active="1-1" class="el-menu-vertical-demo">
      <el-menu-item index="1-1">基本信息</el-menu-item>
      <el-menu-item index="1-2">页面菜单</el-menu-item>
      <el-menu-item index="1-3">数据源</el-menu-item>
    </el-menu>
  </div>
</template>
<style lang="scss">
.app-menu {
  width: 180px;
  background: white;
  flex: none !important;

  .title-part {
    display: flex;
    justify-content: center;
    align-items: center;
  }
}
</style>
<script lang="ts">
  import { Vue, Component, Prop } from "nuxt-property-decorator";

  @Component
  export default class AppItem extends Vue {
    @Prop() app
  }
</script>
