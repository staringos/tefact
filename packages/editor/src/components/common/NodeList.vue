<template>
  <draggable
      class="editor-node-list"
      :group="{ name: 'form-item', pull: 'clone', put: false }"
      :sort="false"
      :list="list"
      @clone="handleClone"
      @change="handleChange"
      @end="handleDragEnd"
  >
    <div
        class="node-item"
        :node="node"
        v-for="(node, i) in list"
        :key="i"
        @click="handleSelect(node.nodeData)"
    >
      <i :class="`tefact-icon ${node.icon}`"></i>
      <span>{{ node.title }}</span>
    </div>
  </draggable>
</template>
<script lang="ts">
import { Component, Prop } from "vue-property-decorator";
import draggable from "vuedraggable";
import { BaseView, DRAGGING_TYPE, IBaseNode } from "@tefact/core"

@Component({
  components: {
    draggable, BaseView
  },
})
export default class NodeList extends BaseView {
  @Prop() list;
  @Prop() subNodeType;

  handleChange() {}

  handleClone(e: any) {
    if (!e) return;
    this.engine.dragging(this.list[e.oldIndex].nodeData, DRAGGING_TYPE.ADD);
  }

  handleDragEnd() {
    this.engine.cleanDragging();
  }

  handleSelect(nodeData: IBaseNode) {
    if (nodeData.type === "ShapeNode" && this.subNodeType !== "shape") {
      this.subNodeType = "shape";
      return;
    }

    let parentId = undefined as any;

    if (this.activeNodeId) {
      if (this.activeNodeType === "section") parentId = this.activeNodeId;
      else parentId = this.engine.activatedNodeParentId;
    }

    if (this.featureType === "form") return this.engine.add(nodeData, -1);
    this.engine.addNode(nodeData, parentId);
  }

}
</script>
