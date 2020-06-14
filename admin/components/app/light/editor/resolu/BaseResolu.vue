<template>
  <el-collapse-item :title="title" :name="index">
    <slot></slot>
  </el-collapse-item>
</template>
<style lang="scss">
  @import "../../../../../assets/styles/variables";

  .base-resolu {
    display: flex;

    /deep/ .el-tabs__content {
      padding-top: 0;

      /deep/ .el-collapse {
        border-top: 0;
      }
    }

    .resolu-title {
      background: $gray-01;
      min-height: 30px;
      line-height: 43px;
      padding-left: 27px;
    }
  }
</style>
<script lang="ts">
  import { Vue, Component, Prop } from "nuxt-property-decorator";

  @Component
  export default class AppItem extends Vue {
    @Prop() title
    @Prop() index
  }
</script>
