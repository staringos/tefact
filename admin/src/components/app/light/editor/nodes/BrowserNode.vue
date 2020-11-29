<template>
  <BaseNode
    v-bind="$attrs"
    v-on="$listeners"
    :node="node"
    :sectionId="sectionId"
    class="button-node"
  >
    <iframe class="node-main" :src="nodeData.src"></iframe>
  </BaseNode>
</template>
<style lang="scss" scoped>
@import "./node.scss";
.node-main {
  border: 0;
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
}
</script>
