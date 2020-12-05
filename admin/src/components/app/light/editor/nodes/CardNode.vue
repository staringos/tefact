<template>
  <BaseNode
    v-bind="$attrs"
    v-on="$listeners"
    :node="node"
    :sectionId="sectionId"
    :preview="preview"
    class="button-node"
  >
    <el-card class="node-main">
      <div slot="header" class="clearfix">
        <span>{{ nodeData.title }}</span>
      </div>
      <div class="card-content">
        {{ nodeData.content }}
      </div>
    </el-card>
  </BaseNode>
</template>
<style lang="scss" scoped>
@import "./node.scss";
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
