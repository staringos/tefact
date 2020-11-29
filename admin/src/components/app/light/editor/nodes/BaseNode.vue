<template>
  <vue-draggable-resizable
    :class="`base-node ${preview ? '' : 'not-preview'}`"
    classNameActive="base-node-active"
    :style="nodeBaseStyle"
    :w="node.config.w"
    :h="node.config.h"
    :x="node.config.x"
    :y="node.config.y"
    :parent="false"
    :debug="false"
    :min-width="50"
    :min-height="50"
    :isConflictCheck="false"
    :snap="true"
    :snapTolerance="10"
    :draggable="!preview"
    :resizable="!preview"
    preventDeactivation
    @click.native.stop
    :active="active"
    @refLineParams="getRefLineParams"
    @update:active="$emit('update:active', $event)"
    @dragging="handleDragging"
    @dragstop="handleDragStop"
    @resizestop="handleResize"
    @keydown="handleKeydown"
  >
    <div class="node-container">
      <slot></slot>
    </div>
  </vue-draggable-resizable>
</template>
<style lang="scss">
  @import "../../../../../assets/styles/variables";

  .base-node {
    display: flex;
    cursor: pointer;
    box-sizing: border-box;
    border: 1px solid transparent;

    &.not-preview {
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
  import { Vue, Component, Prop, namespace } from 'nuxt-property-decorator'
  import VueDraggableResizable from 'vue-draggable-resizable-gorkys'
  import cloneDeep from 'lodash/cloneDeep'
  import { BaseNodeModel, EditorNodeData } from '~/utils/entities/editor/node'

  const editor = namespace('editor')

  @Component({
    components: { VueDraggableResizable }
  })
  export default class BaseNode extends Vue {
    @Prop() node!: BaseNodeModel<EditorNodeData>
    @Prop() preview!: boolean
    @Prop() sectionId!: string
    @Prop() active!: string

    @editor.Action modifyNode

    get nodeBaseStyle() {
      const style = this.node.config.style
      const res = {}

      for (let key in style) {
        if (style.hasOwnProperty(key)) {
          if (key.indexOf('-width') !== -1 || key.indexOf('-size') !== -1) {
            res[key] = `${style[key]}px`
            continue
          }

          res[key] = style[key]
        }
      }

      return res
    }

    handleKeydown(e) {
      console.log('handleKeydown e:', e)
    }

    // 辅助线回调事件
    getRefLineParams (params) {
      this.$emit("onRefLineChange", params)
    }

    handleResize(x, y, w, h) {
      const config = this.node.config
      if (config.x === x && config.y === y && config.w === w && config.h === h) return

      const node = cloneDeep(this.node)
      node.config = { ...this.node.config, x, y, w, h }

      this.modifyNode({ sectionId: this.sectionId, node })
    }

    handleDragStop(x, y) {
      const config = this.node.config
      if (config.x === x && config.y === y) return

      const node = cloneDeep(this.node)
      node.config = { ...this.node.config, x, y }
      this.modifyNode({ sectionId: this.sectionId, node })
    }

    handleDragging() {}
  }
</script>
