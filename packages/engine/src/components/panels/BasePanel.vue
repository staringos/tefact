<template>
  <div class="editor-panel-container">
    <div class="header" v-if="title">
      <i class="el-icon-arrow-left" v-if="hasBack" @click="handleGoBack"></i>
      <span>{{ title }}</span>
    </div>
    <slot></slot>
  </div>
</template>
<script lang="ts">
import { Vue, Component, Prop } from "vue-property-decorator";

@Component({
  components: {}
})
export default class BasePanel extends Vue {
  @Prop(String) title?: string;
  @Prop(Boolean) hasBack?: boolean;

  handleGoBack() {
    this.$emit("back");
  }
}
</script>
<style lang="scss" scoped>
.editor-panel-container {
  overflow: auto;
  width: 160px;
  border-right: 1px solid $borderSecondColor;
  flex: 1;
  display: flex;
  flex-direction: column;
  background: white;

  .header {
    width: 100%;
    height: 32px;
    line-height: 32px;
    text-align: center;
    font-size: 14px;
    font-weight: normal;
    background: $gray-03;
    border-bottom: 1px solid $borderColor;

    .el-icon-arrow-left {
      cursor: pointer;
      float: left;
      line-height: 38px;
      margin-left: 10px;
    }
  }
}
</style>
<style lang="scss">
.editor-panel-container:not(:first-child) {
  .header {
    border-top: 1px solid $borderColor;
  }
}
</style>
