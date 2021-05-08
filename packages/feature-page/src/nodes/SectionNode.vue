<template>
  <div
    :class="`page-section ${!preview ? 'hover-style' : ''} ${
      active && !preview ? 'active' : ''
    }`"
    :style="style"
  >
    <div
      class="page-section-content"
      :group="{
        name: 'form-item',
        pull: engine.draggingType === 'add' ? 'clone' : 'move',
        put: true,
      }"
      :list="[]"
      :style="bgStyle"
      @click="handleSectionClick"
      @start="handleDragStart"
      @end="handleDragEnd"
      @add="handleAdd"
      @change="handleChange"
    >
      <component
        v-for="node in section.children"
        :key="node.id"
        :node="node"
        :sectionId="section.id"
        :is="node.type"
        :preview="preview"
        :sectionConfig="section"
        :active="engine.activeNodeIds.indexOf(node.id) > -1"
        @onRefLineChange="handleRefLineChange"
        @update:active="(active) => handleActiveUpdate(node.id, active)"
        @contextmenu.native="handleContextMenuShow($event, true, node.id)"
        @showBorder="handleBorderLine"
        @hideBorder="handleHideBorder"
      ></component>

      <!--      <transition-group>-->
      <!--      </transition-group>-->

      <NodeContextMenu
        :nodeId="contextNodeId"
        :sectionId="section.id"
        :visible="contextMenuVisible"
        :pos="contextPos"
        @hide="handleContextMenuShow"
      />

      <SectionButtons
        :pageId="pageId"
        :isMobile="isMobile"
        pageType="page"
        :hasAdd="true"
        v-if="active && !preview"
        :index="index"
        :amount="amount"
        :section="section"
      />

      <!-- Assist Line -->
      <span
        class="ref-line v-line"
        v-for="(item, i) in vLine"
        :key="i + 'v'"
        v-show="item.display && !preview"
        :style="{
          left: item.position,
          top: item.origin,
          height: item.lineLength,
        }"
      ></span>
      <span
        class="ref-line h-line"
        v-for="(item, i) in hLine"
        :key="i + 'h'"
        v-show="item.display && !preview"
        :style="{
          top: item.position,
          left: item.origin,
          width: item.lineLength,
        }"
      ></span>

      <span
        class="ref-line border-line h-line"
        v-if="hBorderLineStyle"
        :style="hBorderLineStyle"
      ></span>

      <span
        class="ref-line border-line v-line"
        v-if="vBorderLineStyle"
        :style="vBorderLineStyle"
      ></span>
      <!-- Assist Line END -->
    </div>
  </div>
</template>
<script lang="ts">
import { Component, Prop, Watch } from "vue-property-decorator";
import AddButton from "../components/AddButton.vue";
import nodes from "./";
import { SectionButtons, NodeContextMenu } from "@tefact/ui";
import { BaseView } from "@tefact/core";
import type { IBaseNode } from "@tefact/core";
import { hasMetaKeyPass, transformStyle } from "@tefact/utils";
import draggable from "vuedraggable";
import cloneDeep from "lodash/cloneDeep";

type POS = { x: number; y: number };

@Component({
  components: {
    SectionButtons,
    NodeContextMenu,
    AddButton,
    draggable,
    ...nodes,
  },
})
export default class SectionNode extends BaseView {
  @Prop() section!: IBaseNode;
  @Prop(Boolean) preview!: boolean;
  @Prop() index!: number;
  @Prop(String) pageId!: string;
  @Prop(Boolean) active!: boolean;
  @Prop(Boolean) isMobile!: boolean;
  @Prop(Number) amount!: number;

  contextNodeId: string | null = null;
  contextMenuVisible = false;
  contextPos: POS | null = null;

  vLine = [];
  hLine = [];

  hBorderLineStyle: any = null;
  vBorderLineStyle: any = null;

  get bgStyle() {
    const res = {} as any;
    if (this.setting && this.setting.grid && !this.preview) {
      res.background =
        "linear-gradient(-90deg, rgba(0, 0, 0, 0.1) 1px, transparent 1px) 0% 0% / 20px 20px, linear-gradient(rgba(0, 0, 0, 0.1) 1px, transparent 1px) 0% 0% / 20px 20px";
    }

    return res;
  }

  get style() {
    return transformStyle(this.section);
  }

  @Watch("currentNodesIdsGetter")
  handleCurrentNodesIdsChange() {
    if (!this.activeNodeId) {
      this.handleHideBorder();
    }
  }

  handleChange() {}

  handleAdd(e: any) {
    if (!this.engine.draggingNode) return;

    const newNode = cloneDeep(this.engine.draggingNode);
    this.engine.addNode(newNode, this.section.id);
  }

  handleDragStart() {}

  handleDragEnd() {}

  handleHideBorder() {
    this.hBorderLineStyle = null;
    this.vBorderLineStyle = null;
  }

  handleBorderLine(type: string) {
    let width;
    switch (type) {
      case "top":
        this.hBorderLineStyle = {
          top: 0,
          left: 0,
        };
        break;
      case "bottom":
        this.hBorderLineStyle = {
          top: this.section.pos.h + "px",
          left: 0,
        };
        break;
      case "left":
        this.vBorderLineStyle = {
          top: 0,
          left: 0,
        };
        break;
      case "right":
        width = this.$el.clientWidth;
        this.vBorderLineStyle = {
          top: 0,
          left: width + "px",
        };
        break;
    }
  }

  handleContextMenuShow(e: any, visible: boolean, nodeId: string) {
    if (visible) {
      this.contextNodeId = nodeId;
      this.contextPos = { x: e.clientX, y: e.clientY };
      e.preventDefault();
    }
    // else {
    // this.contextNodeId = null;
    // }
    this.contextMenuVisible = visible;
  }

  handleActiveUpdate(id: string, active: boolean) {
    // const params = { id, active, sectionId: this.section.id };
    if (hasMetaKeyPass()) {
      if (!active) return;
      return this.engine.moreActive(id);
    }

    this.engine.activeNode([id]);
  }

  handleRefLineChange(params: any) {
    const { vLine, hLine } = params;
    this.vLine = vLine;
    this.hLine = hLine;
  }

  handleSectionClick(e: Event) {
    if (this.active) return;
    e.stopPropagation();
    this.$emit("activeChange", this.section.id);
  }

  static NODE = {
    icon: "tf-icon-browser",
    type: "section",
    title: "页面段落",
    showInList: false,
    nodeData: {
      config: {
        h: 500,
        style: {},
      },
      section_type: "editor",
      page_id: null,
      nodes: [],
    },
  };
}
</script>

<style lang="scss" scoped>
.page-section {
  // flex: 1;
  width: 100%;
  min-height: 100px;
  position: relative;
  box-sizing: border-box;
  // border: 1px solid transparent;

  .page-section-content {
    width: 100%;
    height: 100%;
    position: relative;
    box-sizing: border-box;
    flex: 1;
  }

  .border-line {
    &.h-line {
      width: 100%;
    }

    &.v-line {
      height: 100%;
    }
  }

  &.hover-style:hover,
  &.active {
    border: 1px solid $editor-border-active-color;

    ::v-deep .add-button {
      display: flex;
    }
  }

  ::v-deep .add-button {
    display: none;
    position: absolute;
    bottom: -25px;
    left: 50%;
    margin-left: -25px;
  }
}
</style>
