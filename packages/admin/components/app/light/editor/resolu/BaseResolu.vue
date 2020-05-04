<template>
  <el-collapse-item :title="title" :name="index">
    <slot></slot>
  </el-collapse-item>
</template>
<style lang="scss">
  @import "../../../../../assets/styles/variables";

  .base-resolu {
    display: flex;

    .resolu-title {
      background: $gray-01;
      height: 43px;
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
