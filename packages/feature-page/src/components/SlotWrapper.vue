<template>
  <div
    :class="classObj"
    :style="nodeBaseStyle"
    @contextmenu.stop.prevent="handleContextMenu"
    @click.stop="handleActiveUpdate"
  >
    <slot></slot>

    <NodeContextMenu
      :menus="['delete', 'generateWidget']"
      :nodeId="node.id"
      :sectionId="null"
      :visible="contextMenuVisible"
      :pos="contextPos"
      @hide="handleContextMenuShow"
    />
  </div>
</template>
<style lang="scss" scoped>
.slot-wrapper {
  &.editing:hover {
    border: 1px solid $editor-border-active-color;
  }

  &.active {
    border: 1px solid $editor-border-active-color;
  }
}
</style>
<script type="ts">
import { Vue, Component, Prop } from 'nuxt-property-decorator'
import nodes from "../nodes"
import { hasMetaKeyPass } from "@tefact/utils";
import { BaseView } from "@tefact/core"
import { transformStyle } from "@tefact/utils";
import { NodeContextMenu } from "@tefact/ui";

@Component({
  components: {
    ...nodes,
    NodeContextMenu,
  }
})
export default class SlotWrapper extends BaseView {
  contextPos = null;
  contextMenuVisible = false;

  @Prop() className;
  @Prop() preview;
  @Prop() node;

  get editing() {
    return !this.preview;
  }

  get active() {
    return this.node.id === this.activeNodeId;
  }

  get classObj() {
    return {
      'slot-wrapper': true,
      'active': this.active,
      'editing': this.editing,
      ...this.className
    }
  }

  get nodeBaseStyle() {
    if (!this.node) return {};
    const result = transformStyle(this.node);
    result.position = "absolute";
    return result;
  }

  handleContextMenuShow() {
    this.contextMenuVisible = false;
  }

  handleContextMenu(e) {
    this.contextPos = { x: e.clientX, y: e.clientY };
    this.contextMenuVisible = true;
  }

  handleActiveUpdate() {
    if (this.preview) return;

    if (hasMetaKeyPass()) {
      return this.engine.moreActive(this.node.id);
    }

    this.engine.activeNode([this.node.id], 'slot');
  }
}
</script>
