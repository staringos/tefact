<template>
  <BaseNode
    v-bind="$attrs"
    v-on="$listeners"
    :node="node"
    class="table-node"
  >
    <List :entityId="entityId" :section="conditions" :entityParams="entityParams" :entity="section.entity"></List>
  </BaseNode>
</template>
<style lang="scss">
  .table-node {
    display: flex;
  }
</style>
<script lang="ts">
  import { Vue, Component } from "nuxt-property-decorator";
  import List from '../../../../../components/entities/List.vue'
  import NodeClass from '~/components/app/light/editor/nodes/NodeClass'
  import BaseNode from './BaseNode.vue'

  @Component({
    components: {
      List,
      BaseNode
    }
  })
  export default class TableNode extends NodeClass {
    section = {}
    entityParams = {}

    conditions = {}

    entityId = '3b4b2ebc58294149b717dacd912c4dab'
  }
</script>
