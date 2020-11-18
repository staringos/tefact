<template>
  <div :class="`panel ${border && 'panel-bordered'} ${header && `panel-headed`} ${className ? className : ''}`">
    <div class="panel-title" v-if="title">
      {{title}}
      <el-button class="create-btn" v-if="headerButton" :icon="headerButton" @click="handleHeaderButtonClick" circle size="mini"></el-button>
    </div>
    <div :class="`panel-content ${noPadding && `panel-no-padding`}`">
      <slot></slot>
    </div>
  </div>
</template>
<style lang="scss" scoped>
  @import "../theme/variables.scss";

  .panel {
    background-color: #fff;
    flex: 1;
    display: flex;
    flex-direction: column;
    margin: 15px;

    &.panel-bordered {
      border: 1px solid $borderColor;
    }

    &.panel-headed {
      padding-top: 0;

      .panel-title {
        color: $defaultTextColor;
        border-bottom: 1px solid $borderColor;
        padding: 0;
        margin-top: 0;
        margin-bottom: 0;
        font-size: 16px;
        line-height: 46px;
        text-align: center;
      }
    }

    .panel-title {
      font-size: 18px;
      margin-top: 20px;
      margin-bottom: 20px;
      padding-left: 20px;
    }

    .panel-content {
      display: flex;
      flex: 1;
      padding: 10px;
      overflow: auto;
    }

    .panel-no-padding {
      padding: 0 !important;
    }

    .create-btn {
      padding: 7px;
      float: right;
      margin-right: 10px;
      margin-top: 11px;
    }
  }
</style>
<script lang="ts">
  import { Component, Vue, Prop } from 'nuxt-property-decorator'

  @Component
  export default class ArrPanel extends Vue {
    @Prop([String]) title
    @Prop([Boolean]) header
    @Prop([Boolean]) noPadding
    @Prop([Boolean]) border
    @Prop([String]) headerButton
    @Prop([String]) className

    handleHeaderButtonClick() {
      (this as any).$emit('on-header-button-click')
    }
  }
</script>
