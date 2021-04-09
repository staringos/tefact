<template>
  <BaseNode
    v-bind="$attrs"
    v-on="$listeners"
    :node="node"
    :preview="preview"
    class="table-node"
  >
    <!--    <List-->
    <!--      :entityId="node.data.entityId"-->
    <!--      :section="conditions"-->
    <!--      :entityParams="entityParams"-->
    <!--      :entity="section.entity"-->
    <!--    ></List>-->
    <div v-if="!node.data.entityId">
      <span>点击配置</span>
    </div>
  </BaseNode>
</template>
<style lang="scss">
.table-node {
  display: flex;
}
</style>
<script lang="ts">
import { Component } from "vue-property-decorator";
// import List from "../../../../../components/entities/List.vue";
import NodeClass from "./NodeClass";
import BaseNode from "./BaseNode.vue";
import { IBaseNode } from "@tefact/core";

@Component({
  components: {
    // List,
    BaseNode,
  },
})
export default class TableNode extends NodeClass<IBaseNode> {
  section = {};
  entityParams = {};
  conditions = {};
  entityId = "3b4b2ebc58294149b717dacd912c4dab";
}
</script>
