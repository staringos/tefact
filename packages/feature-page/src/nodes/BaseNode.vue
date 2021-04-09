<template>
  <vue-draggable-resizable
    :class="`base-node ${preview ? '' : 'not-preview'}`"
    classNameActive="base-node-active"
    :style="nodeBaseStyle"
    :w="tmpNode.pos.w"
    :h="tmpNode.pos.h"
    :x="tmpNode.pos.x"
    :y="tmpNode.pos.y"
    :parent="false"
    :debug="true"
    :min-width="2"
    :min-height="2"
    :isConflictCheck="false"
    :snap="true"
    :snapTolerance="10"
    :draggable="!preview"
    :resizable="!preview"
    :grid="[20, 20]"
    @resizing="handleResize"
    preventDeactivation
    @click.native.stop
    :active="active"
    @refLineParams="getRefLineParams"
    @update:active="$emit('update:active', $event)"
    @dragging="handleDragging"
    @dragstop="handleDragStop"
    @resize="handleResize"
    @resizestop="handleResizeStop"
    @keydown="handleKeydown"
    @contextmenu.native="handleContextMenu"
  >
    <div class="node-container" @contextmenu="handleContextMenu">
      <slot></slot>
    </div>
  </vue-draggable-resizable>
</template>
<style lang="scss">
.base-node {
  display: flex;
  box-sizing: border-box;
  border: 1px solid transparent;

  &.not-preview {
    cursor: pointer;

    &.base-node-active {
      border-width: 1px !important;
      border: 1px solid $editor-border-focus-color;
    }

    &:hover {
      border-width: 1px !important;
      border: 1px solid $editor-border-active-color;
    }
  }

  ::v-deep .handle {
    z-index: 999;
  }

  .node-container {
    flex: 1;
    display: flex;
    width: 100%;
    height: 100%;
    overflow: hidden;
    box-sizing: border-box;
  }
}
</style>
<script lang="ts">
import { Component, Prop, Watch } from "vue-property-decorator";
import VueDraggableResizable from "vue-draggable-resizable-gorkys";
import cloneDeep from "lodash/cloneDeep";
import isNumber from "lodash/isNumber";
import { transformStyle } from "@tefact/utils";
import { BaseView, IBaseNode, INodePos } from "@tefact/core";

@Component({
  components: { VueDraggableResizable },
})
export default class BaseNode extends BaseView {
  @Prop() node!: IBaseNode;
  @Prop() preview!: boolean;
  @Prop() isShape!: boolean;
  @Prop() sectionId!: string;
  @Prop() active!: boolean;
  @Prop() index!: number;
  @Prop() sectionConfig!: any;

  tmpNode: IBaseNode | null = null;

  @Watch("node", { deep: true, immediate: true })
  handleNodeConfigChange() {
    const { node } = this;
    if (!node) return;
    this.tmpNode = cloneDeep(node);
  }

  get nodeBaseStyle() {
    if (!this.tmpNode) return {};
    const result = transformStyle(this.tmpNode);
    result["z-index"] = this.index;

    if (this.isShape) delete result[`background-color`];
    result.position = "absolute";
    result["z-index"] = this.index;
    return result;
  }

  handleContextMenu() {
    if (this.preview) return;
    this.$emit("context");
  }

  handleKeydown(e: any) {
    console.log("handleKeydown:", e);
  }

  // 辅助线回调事件
  getRefLineParams(params: any) {
    this.$emit("onRefLineChange", params);
  }

  handleResizeStop(x: number, y: number, w: number, h: number) {
    const config = this.node.pos;
    if (config.x === x && config.y === y && config.w === w && config.h === h)
      return;
    this.engine.updateNodePos(this.node.id, { ...this.node.pos, x, y, w, h });
  }

  handleResize(x: number, y: number, w: number, h: number) {
    if (!this.tmpNode) return;
    const curConfig = this.tmpNode.pos;
    if (
      x !== curConfig.x ||
      y !== curConfig.y ||
      w !== curConfig.w ||
      h !== curConfig.h
    ) {
      this.tmpNode = {
        ...this.tmpNode,
        pos: {
          x,
          y,
          w,
          h,
        },
      };
    }
  }

  handleDragStop(x: number, y: number) {
    const config = this.node.pos;
    if (config.x === x && config.y === y) return;
    this.engine.updateNodePos(this.node.id, { ...this.node.pos, x, y });
  }

  handleDragging(x: number, y: number) {
    if (!this.active) return;
    const { sectionConfig, node } = this;
    const pos = node.pos as INodePos;
    const sectionH = isNumber(sectionConfig.pos.h)
      ? sectionConfig.pos.h
      : this.currentTarget.config.style.height;

    if (x >= -1 && x <= 1) return this.$emit("showBorder", "left");

    if (x >= -1 - pos.w && x <= 1 - pos.w)
      return this.$emit("showBorder", "left");

    if (y >= -1 && y <= 1) return this.$emit("showBorder", "top");

    if (y >= -1 - pos.h && y <= 1 - pos.h)
      return this.$emit("showBorder", "top");

    if (y >= sectionH - 1 && y <= sectionH + 1)
      return this.$emit("showBorder", "bottom");

    if (y >= sectionH - pos.h - 1 && y <= sectionH - pos.h + 1)
      return this.$emit("showBorder", "bottom");

    const parentWidth = (this.$el.parentNode as any).clientWidth;

    if (x >= parentWidth - 1 && x <= parentWidth + 1)
      return this.$emit("showBorder", "right");

    if (x >= parentWidth - pos.w - 1 && x <= parentWidth - pos.w + 1)
      return this.$emit("showBorder", "right");
    return this.$emit("hideBorder");
  }
}
</script>
