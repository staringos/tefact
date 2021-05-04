<template>
  <div
    :class="{'slot-position': true, 'dragging': isDragging && !preview, 'empty': node}"
    title="拖拽组件到这里"
    v-if="!node"
  ></div>
  <component
    v-else="node"
    :node="node"
    :is="node.type"
    :preview="preview"
    :active="engine.activeNodeIds.indexOf(node.id) > -1"
    @update:active="(active) => handleActiveUpdate(node.id, active)"
  ></component>
</template>
<style lang="scss" scoped>
.slot-position {
  width: 100%;
  background-color: #00b4ff;
  flex: 1;
  display: flex;

  &.empty {
    height: 0;
  }

  &.dragging {
    height: 30px;
  }
}
</style>
<script lang="ts">
import { Vue, Component, Prop } from 'nuxt-property-decorator'
import nodes from "../nodes"
import get from "lodash/get"
import { hasMetaKeyPass } from "@tefact/utils";
import { BaseView } from "@tefact/core"

@Component({
  components: {
    ...nodes,
  }
})
export default class SlotPosition extends BaseView {
  @Prop() preview
  @Prop() isDragging
  @Prop() slots
  @Prop() name

  get child() {
    return null
  }

  get node() {
    return get(this.slots, this.name)
  }

  handleActiveUpdate(id: string, active: boolean) {
    // const params = { id, active, sectionId: this.section.id };
    if (hasMetaKeyPass()) {
      if (!active) return;
      return this.engine.moreActive(id);
    }

    this.engine.activeNode([id]);
  }
}
</script>
