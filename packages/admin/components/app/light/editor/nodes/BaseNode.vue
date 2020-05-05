<template>
  <vue-draggable-resizable
    class="base-node"
    :style="nodeBaseStyle"
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

    /deep/ .handle {
      z-index: 999;
    }

    .node-container {
      flex: 1;
      width: 100%;
      height: 100%;
      overflow: hidden;
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

    // 辅助线回调事件
    getRefLineParams (params) {
      this.$emit("onRefLineChange", params)
    }

    handleResize(x, y, w, h) {
      const config = this.node.config
      if (config.x === x && config.y === y && config.w === w && config.h === h) return

      const node = _.cloneDeep(this.node)
      node.config = { ...this.node.config, x, y, w, h }

      this.modifyNode({ sectionId: this.sectionId, node })
    }

    handleDragStop(x, y) {
      const config = this.node.config
      if (config.x === x && config.y === y) return

      const node = _.cloneDeep(this.node)
      node.config = { ...this.node.config, x, y }
      this.modifyNode({ sectionId: this.sectionId, node })
    }

    handleDragging() {

    }
  }
</script>
