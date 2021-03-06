<template>
  <BasePanel class="layers-panel" title="图层">
    <el-tree
      class="layers-panel-tree"
      ref="tree"
      :data="data"
      node-key="id"
      :expand-on-click-node="false"
      :allow-drop="allowDrop"
      :allow-drag="allowDrag"
      draggable
      default-expand-all
      highlight-current
      @current-change="handleCurrentChange"
      @node-drop="handleNodeDrop"
    >
      <span class="custom-tree-node" slot-scope="{ node, data }">
        <span>{{ node.label }}</span>
        <span>
          <el-button
            type="text"
            size="mini"
            icon="el-icon-delete"
            @click="() => handleRemove(data)"
          >
          </el-button>
        </span>
      </span>
    </el-tree>
  </BasePanel>
</template>
<style lang="scss" scoped>
.layers-panel-tree {
  overflow: auto;

  .custom-tree-node {
    font-size: 12px;
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding-right: 8px;

    &.active {
      background-color: $gray-05;
    }
  }
}
</style>
<script lang="ts">
import { Component, Watch } from "vue-property-decorator";
import BasePanel from "TEFACT_EDITOR/components/panels/BasePanel.vue";
import { IBaseNode, BaseView } from "@tefact/core";
import cloneDeep from "lodash/cloneDeep";

type LayerMenuItem = {
  id?: string;
  label?: string;
  type?: string;
  children?: Array<LayerMenuItem>;
};

function wrapChildren(data) {
  return data.map((cur) => {
    if (cur.children && cur.children.length > 0) {
      cur.data.children = wrapChildren(cur.children);
    }
    return cur.data;
  });
}

@Component({
  components: { BasePanel },
})
export default class LayersPanel extends BaseView {
  data = [] as Array<LayerMenuItem>;

  @Watch("engine.target", { immediate: true, deep: true })
  handlePageChange() {
    const newData = [] as Array<LayerMenuItem>;
    const activeId = this.activatedNode?.id;
    const isForm = this.featureType === "form";
    const nodes = this.currentTarget?.config?.children;
    if (!nodes) return;
    nodes.forEach((cur) => {
      let children = [] as Array<IBaseNode>;

      if (!isForm) {
        children =
          cur.children?.map((node) => {
            return {
              id: node.id,
              label: node.type,
              active: node.id === activeId,
              sectionId: cur.id,
              data: node,
              type: node.type,
            } as any;
          }) || [];
      }
      newData.push({
        id: cur.id,
        label: isForm ? cur.type : "段落",
        type: isForm ? cur.type : "section",
        active: cur.id === activeId,
        data: cur,
        children,
      } as LayerMenuItem);
    });

    this.data = newData;
  }

  handleCurrentChange(node: IBaseNode) {
    this.engine.activeNode([node.id]);
  }

  @Watch("currentNode")
  handleNodeChange() {
    this.watchChange();
  }

  @Watch("activeNode")
  handleSectionChange() {
    this.watchChange();
  }

  allowDrag() {
    return true;
  }

  allowDrop(draggingNode: any, dropNode: any, type: string) {
    const dragType = draggingNode.data.type;
    const dropType = dropNode.data.type;
    if (dragType === "section" && type !== "inner") {
      return false;
    }

    if (dragType !== "section" && dropType !== "section") {
      return false;
    }

    if (dropType === "section" && (type === "next" || type === "prev")) {
      return false;
    }

    if (dropType !== "section" && dragType === "section") {
      return false;
    }

    return true;
  }

  watchChange() {
    const cur = this.activeNodeId;
    if (!cur) return;
    (this.$refs.tree as any).setCurrentKey(cur);
  }

  handlePlus() {}

  handleNodeDrop() {
    return this.engine.replaceChildren(wrapChildren(cloneDeep(this.data)));
  }

  async handleRemove(node: IBaseNode) {
    this.engine.deleteNode(node.id);
  }
}
</script>
