<template>
  <div
    :class="classObj"
    :style="nodeBaseStyle"
    @click.stop="handleActiveUpdate"
  >
    <slot></slot>
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
import get from "lodash/get"
import { hasMetaKeyPass } from "@tefact/utils";
import { BaseView } from "@tefact/core"
import { transformStyle } from "@tefact/utils"

@Component({
  components: {
    ...nodes,
  }
})
export default class SlotWrapper extends BaseView {
  @Prop() className
  @Prop() preview
  @Prop() node

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

  handleActiveUpdate() {
    if (hasMetaKeyPass()) {
      return this.engine.moreActive(this.node.id);
    }

    this.engine.activeNode([this.node.id], 'slot');
  }
}
</script>
