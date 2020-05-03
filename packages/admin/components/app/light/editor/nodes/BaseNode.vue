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
    @refLineParams="getRefLineParams">
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
  import { Vue, Component, Prop } from 'nuxt-property-decorator'
  import VueDraggableResizable from 'vue-draggable-resizable-gorkys'
  import { BaseNodeModel } from '~/utils/entities/editor/node'

  @Component({
    components: { VueDraggableResizable }
  })
  export default class BaseNode extends Vue {
    @Prop() node?: BaseNodeModel
    // 辅助线回调事件
    getRefLineParams (params) {
      this.$emit("onRefLineChange", params)
    }
  }
</script>
