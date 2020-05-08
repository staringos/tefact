<template>
  <BaseNode
    v-bind="$attrs"
    v-on="$listeners"
    :node="node"
    :sectionId="sectionId"
    class="table-node"
  >
    <List :section="section" :entityParams="entityParams" :entity="section.entity"></List>
  </BaseNode>
</template>
<style lang="scss">

</style>
<script lang="ts">
  import { Vue, Component } from "nuxt-property-decorator";
  import List from '~/components/entities/List.vue'
  import NodeClass from '~/components/app/light/editor/nodes/NodeClass'
  import BaseNode from './BaseNode.vue'

  @Component({
    components: {
      List, BaseNode
    }
  })
  export default class TableNode extends NodeClass {
    section = {}
    entityParams = {}
  }
</script>
