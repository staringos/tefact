<template>
  <vue-draggable-resizable
    :class="`base-node ${preview ? '' : 'not-preview'}`"
    classNameActive="base-node-active"
    :style="nodeBaseStyle"
    :w="tmpConfig.w"
    :h="tmpConfig.h"
    :x="tmpConfig.x"
    :y="tmpConfig.y"
    :parent="false"
    :debug="false"
    :min-width="2"
    :min-height="2"
    :isConflictCheck="false"
    :snap="true"
    :snapTolerance="10"
    :draggable="!preview"
    :resizable="!preview"
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
@import "../../../../../assets/styles/variables";

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
import { Vue, Component, Prop, Watch } from "vue-property-decorator";
import VueDraggableResizable from "vue-draggable-resizable-gorkys";
import cloneDeep from "lodash/cloneDeep";
import { transformStyle } from "@tefact/utils";
import { BaseView, IBaseNode } from "@tefact/core";

// const editor = namespace("editor");

@Component({
  components: { VueDraggableResizable },
})
export default class BaseNode extends BaseView {
  @Prop() node!: IBaseNode;
  @Prop() preview!: boolean;
  @Prop() isShape!: boolean;
  @Prop() sectionId!: string;
  @Prop() active!: string;
  @Prop() index!: number;
  @Prop() sectionConfig!: any;

  // @editor.Action modifyNode;

  tmpConfig: IBaseNode | null = null;

  @Watch("node.config", { deep: true, immediate: true })
  handleNodeConfigChange() {
    const { node } = this;
    if (!node) return;
    this.tmpConfig = cloneDeep(node);
  }

  get nodeBaseStyle() {
    if (!this.tmpConfig) return {};
    const result = transformStyle(this.tmpConfig);
    result["z-index"] = this.index;

    if (this.isShape) delete result[`background-color`];
    return result;
  }

  handleContextMenu() {
    if (this.preview) return;
    this.$emit("context");
  }

  handleKeydown(e: any) {
    console.log("handleKeydown e:", e);
  }

  // 辅助线回调事件
  getRefLineParams(params: any) {
    this.$emit("onRefLineChange", params);
  }

  handleResizeStop(x: number, y: number, w: number, h: number) {
    const config = this.node.pos;
    if (config.x === x && config.y === y && config.w === w && config.h === h)
      return;

    const node = cloneDeep(this.node);
    node.pos = { ...this.node.pos, x, y, w, h };

    this.engine.updateNode(node);
  }

  handleResize(x: number, y: number, w: number, h: number) {
    if (!this.tmpConfig) return;
    const curConfig = this.tmpConfig.pos;
    if (
      x !== curConfig.x ||
      y !== curConfig.y ||
      w !== curConfig.w ||
      h !== curConfig.h
    ) {
      this.tmpConfig = {
        ...this.tmpConfig,
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

    const node = cloneDeep(this.node);
    node.pos = { ...this.node.pos, x, y };
    this.engine.updateNode(node);
  }

  handleDragging(x: number, y: number, w: number, h: number) {
    if (!this.active) return;
    const { sectionConfig, node } = this;

    if (x >= -1 && x <= 1) {
      return this.$emit("showBorder", "left");
    }

    if (x >= -1 - node.pos.w && x <= 1 - node.pos.w) {
      return this.$emit("showBorder", "left");
    }

    if (y >= -1 && y <= 1) {
      return this.$emit("showBorder", "top");
    }

    if (y >= -1 - node.pos.h && y <= 1 - node.pos.h) {
      return this.$emit("showBorder", "top");
    }

    if (y >= sectionConfig.h - 1 && y <= sectionConfig.h + 1) {
      return this.$emit("showBorder", "bottom");
    }

    if (
      y >= sectionConfig.h - node.pos.h - 1 &&
      y <= sectionConfig.h - node.pos.h + 1
    ) {
      return this.$emit("showBorder", "bottom");
    }

    const parentWidth = (this.$el.parentNode as any).clientWidth;

    if (x >= parentWidth - 1 && x <= parentWidth + 1) {
      return this.$emit("showBorder", "right");
    }

    if (
      x >= parentWidth - node.pos.w - 1 &&
      x <= parentWidth - node.pos.w + 1
    ) {
      return this.$emit("showBorder", "right");
    }

    return this.$emit("hideBorder");
  }
}
</script>
