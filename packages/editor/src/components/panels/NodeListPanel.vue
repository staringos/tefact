<template>
  <BasePanel
    class="editor-node-list-wrapper"
    :title="editorDetails.title || '元素'"
    :hasBack="editorDetails.hasGoBack"
    @back="handleGoBack"
    @click.stop
  >
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
        v-for="(node, i) in editorDetails.list"
        :key="i"
        @click="handleSelect(node.nodeData)"
      >
        <i :class="`tefact-icon ${node.icon}`"></i>
        <span>{{ node.title }}</span>
      </div>
    </draggable>
  </BasePanel>
</template>
<script lang="ts">
import { Component } from "vue-property-decorator";
import { FORM_NODE_LIST, PAGE_NODE_LIST } from "@/components/features";
import { Shape, BaseView, DRAGGING_TYPE } from "@tefact/core";
import draggable from "vuedraggable";
import BasePanel from "@/components/panels/BasePanel.vue";
import { IBaseNode, NodeListConfig } from "@tefact/core";

const EditorNodesDetails = {
  shape: {
    title: "图形",
    hasGoBack: true,
    list: Shape.SHAPE_NODE_LIST
  },
  form: {
    title: "表单",
    hasGoBack: false,
    list: FORM_NODE_LIST
  },
  page: {
    title: null,
    hasGoBack: false,
    list: PAGE_NODE_LIST
  },
  default: {
    title: null,
    hasGoBack: false,
    list: PAGE_NODE_LIST
  }
} as Record<string, NodeListConfig>;

@Component({
  components: {
    BasePanel,
    draggable
  }
})
export default class NodeList extends BaseView {
  curDraggingNode: any | null = null;
  subNodeType: string | null = null;

  get editorDetails(): NodeListConfig {
    if (this.subNodeType) return EditorNodesDetails[this.subNodeType];
    return (
      EditorNodesDetails[this.currentTarget.featureType] ||
      EditorNodesDetails.default
    );
  }

  get list() {
    return Object.values(this.editorDetails.list);
  }

  handleChange() {}

  handleClone(e: any) {
    if (!e) return;
    console.log("e:", e);
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

    let parentId = undefined;

    if (this.activeNodeId) {
      if (this.activeNodeType === "section") parentId = this.activeNodeId;
      else parentId = this.engine.activatedNodeParentId;
    }

    this.engine.addNode(nodeData, parentId);
  }

  handleGoBack() {
    this.subNodeType = null;
  }
}
</script>
<style lang="scss">
.editor-node-list-wrapper {
  .header {
    width: 100%;
    height: 38px;
    line-height: 38px;
    text-align: center;
    font-size: 16px;
    font-weight: normal;
    border-bottom: 1px solid $borderColor;

    .el-icon-arrow-left {
      cursor: pointer;
      float: left;
      line-height: 38px;
      margin-left: 10px;
    }
  }

  .editor-node-list {
    display: flex;
    flex-direction: row;
    padding: 10px;
    flex-wrap: wrap;

    .node-item {
      width: 70px;
      height: 70px;
      border-radius: 3px;
      display: flex;
      justify-content: center;
      align-items: center;
      flex-direction: column;
      cursor: pointer;
      user-select: none;
      box-sizing: border-box;

      i {
        font-size: 20px;
        color: $mainColor;
      }

      span {
        font-size: 12px;
        color: $textMainColor;
        margin-top: 5px;
      }

      &:hover {
        color: $secondColor;
        border: 1px solid $editor-node-border-color;
      }
    }
  }
}
</style>
