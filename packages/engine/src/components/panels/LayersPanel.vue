<template>
  <BasePanel class="layers-panel" title="图层">
    <el-tree
      class="layers-panel-tree"
      :data="data"
      node-key="id"
      :expand-on-click-node="false"
      @current-change="handleCurrentChange"
      ref="tree"
      default-expand-all
      highlight-current
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
import BasePanel from "@/components/panels/BasePanel.vue";
import { BaseView } from "@/engine";
import { IBaseNode } from "@tefact/common";

type LayerMenuItem = {
  id?: string;
  label?: string;
  type?: string;
  children?: Array<LayerMenuItem>;
};

@Component({
  components: { BasePanel }
})
export default class LayersPanel extends BaseView {
  data = [] as Array<LayerMenuItem>;

  // @editor.Getter currentPage
  // @editor.Getter currentNode
  // @editor.Getter currentSectionIdGetter
  // @editor.Action chooseSection
  // @editor.Action activeNode
  // @editor.Action chooseNode
  // @editor.Action deleteNode
  // @editor.Action deleteSection

  @Watch("currentPage", { immediate: true, deep: true })
  handlePageChange() {
    const newData = [] as Array<LayerMenuItem>;
    const activeId = this.activeNode?.id;
    const isForm = this.featureType === "form";
    const nodes = this.currentTarget?.config?.children;
    if (!nodes) return;
    nodes.forEach(cur => {
      let children = [] as Array<IBaseNode>;

      if (!isForm) {
        children =
          cur.children?.map(node => {
            return {
              id: node.id,
              label: node.type,
              active: node.id === activeId,
              sectionId: cur.id,
              type: node.type
            } as any;
          }) || [];
      }
      newData.push({
        id: cur.id,
        label: isForm ? cur.type : "段落",
        type: isForm ? cur.type : "section",
        active: cur.id === activeId,
        children
      } as LayerMenuItem);
    });

    this.data = newData;
  }

  // @Watch("currentSectionIdGetter")
  handleCurrentChange(node: IBaseNode) {
    this.engine.active([node.id]);
  }

  @Watch("currentNode")
  handleNodeChange() {
    this.watchChange();
  }

  @Watch("activeNode")
  handleSectionChange() {
    this.watchChange();
  }

  watchChange() {
    const cur = this.activeNodeId;
    if (!cur) return;
    (this.$refs.tree as any).setCurrentKey(cur);
  }

  handlePlus() {}
  async handleRemove(node: IBaseNode) {
    this.engine.deleteNode(node.id);
  }
}
</script>
