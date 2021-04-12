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
import { Component, Prop } from "vue-property-decorator";
import { BaseView } from "@tefact/core";
import type { IBaseNode } from "@tefact/core";
import { Properties as PageProperties } from "@tefact/feature-page";

@Component
export default class SectionButtons extends BaseView {
  @Prop(Number) index!: number;
  @Prop(Number) amount!: number;
  @Prop(String) pageId!: string;
  @Prop(String) pageType!: string;
  @Prop(Boolean) hasAdd!: boolean;
  @Prop(Boolean) isMobile!: boolean;
  @Prop(Object) section!: IBaseNode;

  handleAdd() {
    if (!this.engine.target) return;
    this.engine.add(
      PageProperties.defaultPageSections(this.engine.target.displayType),
      this.index + 1
    );
  }

  handleDelete() {
    this.engine.deleteNode(this.section.id);
  }

  handleSectionIndex(index: number) {
    this.engine.resetNodeOrder(this.section.id, index);
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
