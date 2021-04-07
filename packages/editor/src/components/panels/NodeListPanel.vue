<template>
  <BasePanel
    class="editor-node-list-wrapper"
    :title="editorDetails.title || '元素'"
    :hasBack="editorDetails.hasGoBack"
    @back="handleGoBack"
    @click.stop
  >
    <NodeList v-if="!hasCategory" :list="list" :subNodeType="subNodeType" />
<!--    <draggable-->
<!--      class="editor-node-list"-->
<!--      v-if="hasCategory"-->
<!--      :group="{ name: 'form-item', pull: 'clone', put: false }"-->
<!--      :sort="false"-->
<!--      :list="list"-->
<!--      @clone="handleClone"-->
<!--      @change="handleChange"-->
<!--      @end="handleDragEnd"-->
<!--    >-->
<!--      <div-->
<!--        class="node-item"-->
<!--        :node="node"-->
<!--        v-for="(node, i) in editorDetails.list"-->
<!--        :key="i"-->
<!--        @click="handleSelect(node.nodeData)"-->
<!--      >-->
<!--        <i :class="`tefact-icon ${node.icon}`"></i>-->
<!--        <span>{{ node.title }}</span>-->
<!--      </div>-->
<!--    </draggable>-->
    <template v-else>
      <div
        class="classified-node-list"
        v-for="(category, i) in editorDetails.categories"
        :key="i"
      >
        <div class="classified-node-header">
          {{category}}
        </div>
        <NodeList v-if="editorDetails.classifiedList" :list="editorDetails.classifiedList[category]" :subNodeType="subNodeType" />
      </div>
    </template>
  </BasePanel>
</template>
<script lang="ts">
import { Component } from "vue-property-decorator";
import {
  FORM_NODE_LIST,
  PAGE_NODE_LIST,
  FORM_NODE_CATEGORIES,
} from "TEFACT_EDITOR/components/features";
import { Shape, BaseView } from "@tefact/core";
import BasePanel from "TEFACT_EDITOR/components/panels/BasePanel.vue";
import type { NodeListConfig } from "@tefact/core";
import groupBy from "lodash/groupBy";
import NodeList from "../common/NodeList.vue"

const EditorNodesDetails = {
  shape: {
    title: "图形",
    hasGoBack: true,
    list: Object.values(Shape.SHAPE_NODE_LIST),
  },
  form: {
    title: "表单",
    hasGoBack: false,
    categories: FORM_NODE_CATEGORIES,
    list: Object.values(FORM_NODE_LIST),
  },
  page: {
    title: null,
    hasGoBack: false,
    list: Object.values(PAGE_NODE_LIST),
  },
  default: {
    title: null,
    hasGoBack: false,
    list: Object.values(PAGE_NODE_LIST),
  },
} as Record<string, NodeListConfig>;

@Component({
  components: {
    NodeList,
    BasePanel
  },
})
export default class NodeListPanel extends BaseView {
  curDraggingNode: any | null = null;
  subNodeType: string | null = null;

  get editorDetails(): NodeListConfig {
    let curDetails: NodeListConfig | null = null;
    if (this.subNodeType) {
      curDetails = EditorNodesDetails[this.subNodeType];
    } else {
      curDetails = (
          EditorNodesDetails[this.currentTarget.featureType] ||
          EditorNodesDetails.default
      );
    }

    if (curDetails.categories) {
      const res = groupBy(Object.values(curDetails.list), "category");
      curDetails.classifiedList = res as any;
    }

    return curDetails;
  }

  get hasCategory(): boolean {
    if (!this.editorDetails) return false;
    if (!this.editorDetails.categories) return false;
    return this.editorDetails.categories.length > 0;
  }

  get list() {
    return this.editorDetails.list;
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

  .classified-node-header {
    text-align: center;
    font-size: 12px;
    margin-top: 10px;
  }
}
</style>
