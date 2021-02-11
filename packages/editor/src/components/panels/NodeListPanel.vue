<template>
  <BasePanel
    class="editor-node-list-wrapper"
    :title="editorDetails.title || '元素'"
    :hasBack="activeNodeType === 'shape'"
    @back="handleGoBack"
    @click.stop
  >
    <draggable
      class="editor-node-list"
      :group="{ name: 'form-item', pull: 'clone', put: false }"
      :clone="handleClone"
      :sort="false"
      @end="handleDragEnd"
      @change="handleChange"
      :list="list"
    >
      <div
        class="node-item"
        :node="node"
        v-for="(node, i) in editorDetails.list"
        :key="i"
        @click="handleAddNode(node.nodeData)"
      >
        <i :class="`tefact-icon ${node.icon}`"></i>
        <span>{{ node.title }}</span>
      </div>
    </draggable>
  </BasePanel>
</template>
<script lang="ts">
import { Component } from "vue-property-decorator";
import cloneDeep from "lodash/cloneDeep";
import { FORM_NODE_LIST, PAGE_NODE_LIST } from "@/components/features";
import { Shape, BaseView } from "@tefact/core";
import draggable from "vuedraggable";
import BasePanel from "@/components/panels/BasePanel.vue";
import { IBaseNode, NodeListConfig } from "@tefact/core";

const EditorNodesDetails = {
  shape: {
    title: "图形",
    list: Shape.SHAPE_NODE_LIST
  },
  form: {
    title: "表单",
    list: FORM_NODE_LIST
  },
  page: {
    title: null,
    list: PAGE_NODE_LIST
  },
  default: {
    title: null,
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
  // @editor.Action addNode;
  // @editor.Action addFormNode;

  // subNodeType: string | null = null;
  curDraggingNode: any | null = null;

  get editorDetails(): NodeListConfig {
    console.log("this.activeNodeType:", this.activeNodeType);
    if (this.activeNodeType && EditorNodesDetails[this.activeNodeType])
      return EditorNodesDetails[this.activeNodeType];
    return this.featureType
      ? EditorNodesDetails[super.featureType]
      : EditorNodesDetails["default"];
  }

  get list() {
    return Object.values(this.editorDetails.list);
  }

  handleChange() {}

  handleClone(e: any) {
    this.curDraggingNode = e;
  }

  handleDragEnd(e: any) {
    if (!this.curDraggingNode) return;
    this.handleAddNode(this.curDraggingNode.nodeData, e.newIndex);
    this.curDraggingNode = null;
  }

  handleAddNode(nodeData: IBaseNode, index = -1) {
    // if (this.editorType === "form") {
    //   return this.addFormNode({ node: cloneDeep(nodeData), index });
    // }
    this.engine.add(cloneDeep(nodeData), index);
  }

  handleGoBack() {}
}
</script>
<style lang="scss">
.editor-node-list-wrapper {
  //overflow: auto;
  //width: 160px;
  //background: #fff;
  //border-right: 1px solid $borderSecondColor;

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
