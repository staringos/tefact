<template>
  <BaseNode
    v-bind="$attrs"
    v-on="$listeners"
    :node="node"
    :sectionId="sectionId"
    :preview="preview"
    class="form-node"
  >
    <Form :form="form" />
  </BaseNode>
</template>
<style lang="scss" scoped>
@import "../../../../../assets/styles/variables";

.form-node {
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: $gray-01;
  position: relative;

  .main {
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
import Form from "~/components/app/light/editor/Form.vue"
import cloneDeep from 'lodash/cloneDeep'
import { DefaultForm } from "~/utils/entities/editor/form"

const editor = namespace('editor')
const system = namespace('system')

@Component({
  components: { Form, BaseNode }
})
export default class FormNode extends NodeClass<ButtonNodeModel> {
  editor: any = null
  form = cloneDeep(DefaultForm)

  @system.Getter uploadUrl
  @editor.Action modifyNode

  handleClick() {
    if (this.nodeData.link) {
      location.href = this.nodeData.link;
    }
  }
}
</script>
