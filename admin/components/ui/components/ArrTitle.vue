<template>
  <h2 :class="`title title-${size} ${bordered && 'bordered'}`">
    <slot></slot>
  </h2>
</template>
<style lang="scss" scoped>
  @import "../theme/variables";

  .title {
    font-weight: 400;
    color: rgba(23,23,37,1);
    line-height: 22px;
    margin-bottom: 20px;
    margin-top: 20px;
    font-size: 16px;

    &.bordered {
      border-left: 5px solid $mainColor;
      padding-left: 10px;
      font-weight: 500;
    }

    &.title-h2 { font-size: 26px; }
    &.title-h3 { font-size: 16px; }
    &.title-h4 { font-size: 14px; }
  }
</style>
<script lang="ts">
  import { Component, Vue, Prop, Emit } from 'nuxt-property-decorator'

  @Component
  export default class ArrTitle extends Vue {
    @Prop(String) size
    @Prop(Boolean) bordered
  }
</script>
