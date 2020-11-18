<template>
  <BaseNode
    v-bind="$attrs"
    v-on="$listeners"
    :node="node"
    :sectionId="sectionId"
    class="button-node"
  >
    <el-button class="button-node-main" :style="{width: config.w, height: config.h}" v-bind="nodeData" @click="handleClick">{{nodeData.text}}</el-button>
  </BaseNode>
</template>
<style lang="scss" scoped>
@import "../../../../../assets/styles/variables";

.button-node {
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: $gray-01;
  position: relative;

  .button-node-main {
    width: 100%;
    height: 100%;
  }
}
</style>
<script lang="ts">
import { Component, namespace } from 'nuxt-property-decorator'
import BaseNode from './BaseNode.vue'
import NodeClass from "~/components/app/light/editor/nodes/NodeClass";
import { ButtonNodeModel } from "~/utils/entities/editor/node"

const editor = namespace('editor')
const system = namespace('system')

@Component({
  components: { BaseNode }
})
export default class ImageNode extends NodeClass<ButtonNodeModel> {
  editor: any = null

  @system.Getter uploadUrl
  @editor.Action modifyNode

  handleClick() {
    if (this.nodeData.link) {
      location.href = this.nodeData.link;
    }
  }
}
</script>
