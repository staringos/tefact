<template>
  <vue-draggable-resizable
    class="base-node"
    :w="node.config.w"
    :h="node.config.h"
    :x="node.config.x"
    :y="node.config.y"
    :parent="true"
    :debug="false"
    :min-width="50"
    :min-height="50"
    :isConflictCheck="true"
    :snap="true"
    :snapTolerance="10"
    @refLineParams="getRefLineParams"
    :draggable="!preview"
    :resizable="!preview"
    @update:active="$emit('update:active', $event)"
    @dragging="handleDragging"
    @dragstop="handleDragStop"
    @resizestop="handleResize"
  >
    <div class="node-container">
      <slot></slot>
    </div>
  </vue-draggable-resizable>
</template>
<style lang="scss">
  .base-node {
    background: #fff;
    display: flex;
    cursor: pointer;

    .node-container {
      flex: 1;
    }
  }
</style>
<script lang="ts">
  import { Vue, Component, Prop, namespace } from 'nuxt-property-decorator'
  import VueDraggableResizable from 'vue-draggable-resizable-gorkys'
  import _ from 'lodash'
  import { BaseNodeModel } from '~/utils/entities/editor/node'

  const editor = namespace('editor')

  @Component({
    components: { VueDraggableResizable }
  })
  export default class BaseNode extends Vue {
    @Prop() node!: BaseNodeModel
    @Prop() preview!: boolean
    @Prop() sectionId!: string

    @editor.Action modifyNode

    // 辅助线回调事件
    getRefLineParams (params) {
      this.$emit("onRefLineChange", params)
    }

    handleResize(x, y, w, h) {
      const node = _.cloneDeep(this.node)
      node.config = { ...this.node.config, x, y, w, h }

      console.log("handleResize node:", node)
      this.modifyNode({ sectionId: this.sectionId, node })
    }

    handleDragStop(x, y) {
      const node = _.cloneDeep(this.node)
      node.config = { ...this.node.config, x, y }
      this.modifyNode({ sectionId: this.sectionId, node })
    }

    handleDragging() {

    }
  }
</script>
