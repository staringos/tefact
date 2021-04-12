<template>
  <div class="add-button" v-show="show" @click="handleAddPageSection">
    <i class="el-icon-plus"></i>
  </div>
</template>
<style lang="scss" scoped>
.add-button {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background-color: $editor-main-color;
  margin: 0 auto;
  justify-content: center;
  align-items: center;
  display: flex;
  cursor: pointer;
  z-index: 999;

  .el-icon-plus {
    color: white;
    font-weight: bold;
    font-size: 16px;
  }
}
</style>
<script lang="ts">
import { Component, Prop } from "vue-property-decorator";
import { BaseView } from "@tefact/core";
import { Properties as PageProperties } from "@tefact/feature-page";

// const editor = namespace("editor");

@Component
export default class AddButton extends BaseView {
  @Prop() index!: number;
  @Prop() pageId!: string;
  @Prop([Boolean]) show!: boolean;

  // @editor.Action addPageSection;

  handleAddPageSection() {
    this.engine.add(PageProperties.defaultPageSections(this.engine.target.displayType), this.index);
  }
}
</script>
