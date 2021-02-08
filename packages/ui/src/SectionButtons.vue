<template>
  <div class="option-buttons">
    <el-button
      type="default"
      size="mini"
      icon="el-icon-top"
      @click="handleSectionIndex(index - 1)"
      v-if="index !== 0"
      circle
    ></el-button>
    <el-button
      type="default"
      size="mini"
      icon="el-icon-bottom"
      @click="handleSectionIndex(index + 1)"
      v-if="index !== amount - 1"
      circle
    ></el-button>
    <el-button
      type="danger"
      size="mini"
      icon="el-icon-delete"
      @click="handleDelete"
      circle
    ></el-button>
    <el-button
      v-if="hasAdd"
      type="primary"
      size="mini"
      icon="el-icon-plus"
      @click="handleAdd"
      circle
    ></el-button>
  </div>
</template>
<script lang="ts">
import { Vue, Component, Prop } from "vue-property-decorator";
import { BaseView, IBaseNode } from "@tefact/core";

// const editor = namespace("editor");

@Component
export default class SectionButtons extends BaseView {
  @Prop(Number) index!: number;
  @Prop(Number) amount!: number;
  @Prop(String) pageId!: string;
  @Prop(String) pageType!: string;
  @Prop(Boolean) hasAdd!: boolean;
  @Prop(Boolean) isMobile!: boolean;
  @Prop(Object) section!: IBaseNode;

  // @editor.Action setSectionIndex;
  // @editor.Action deleteSection;
  // @editor.Action addPageSection;

  handleAdd() {
    if (this.pageType === "page")
      this.engine.add({ index: this.index, pageId: this.pageId });
  }

  handleDelete() {
    this.engine.delete(this.section.id);
  }

  handleSectionIndex(index) {
    this.engine.reOrderNode(this.section.id, index);
  }
}
</script>
<style lang="scss" scoped>
.option-buttons {
  display: flex;
  margin-bottom: -14px;
  z-index: 999;
  height: 28px;
  position: absolute;
  width: 100%;
  justify-content: center;
  bottom: 0;
}
</style>
