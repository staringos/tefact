<template>
  <div :class="{'page-canvas-container': true, 'tab-bar-page': hasTabBar, 'header-bar-page': hasHeaderBar}">
    <SlotPosition :slots="slots" name="HeaderBar" :preview="preview" />
    <div
      :class="`editor-page-canvas ${direction}-side`"
      :style="style"
      @click="handlePageClick"
    >
      <div class="section section-add" v-if="!sections || sections.length < 1">
        <AddButton :index="0" :pageId="pageId" show></AddButton>
      </div>
      <PageSection
        v-for="(section, i) in sections"
        :key="section.id"
        :index="i"
        :section="section"
        :pageId="pageId"
        :preview="preview"
        :isMobile="isMobile"
        :amount="sections.length"
        :active="activeNodeId === section.id"
        @activeChange="handleActiveChange(section.id)"
      ></PageSection>
    </div>
    <SlotPosition :slots="slots" name="TabBar" :preview="preview" />
  </div>
</template>
<script lang="ts">
import { Component, Prop, Watch } from "vue-property-decorator";
import { addListener, removeListener } from "resize-detector";

import "vue-draggable-resizable-gorkys/dist/VueDraggableResizable.css";
import PageSection from "./nodes/SectionNode.vue";
import TabBarNode from "./nodes/TabBarNode.vue";
import AddButton from "./components/AddButton.vue";
import cloneDeep from "lodash/cloneDeep";
import get from "lodash/get";
import { transformStyle } from "@tefact/utils";
import { BaseView } from "@tefact/core";
import type { ISetting, ITarget } from "@tefact/core";
import HeaderBarNode from "./nodes/HeaderBarNode.vue"
import SlotPosition from "./components/SlotPosition.vue"

@Component({
  components: {
    SlotPosition,
    HeaderBarNode,
    AddButton,
    PageSection,
    TabBarNode,
  },
})
export default class Page extends BaseView {
  @Prop() pageId!: string;
  @Prop() page!: ITarget;
  @Prop() editorSetting!: ISetting;
  @Prop({ type: String, default: "pc" }) device!: string;
  @Prop(Boolean) preview!: boolean;
  @Prop(Boolean) isMobile!: boolean;

  style = {} as Record<string, any>;

  get activeNodeIds() {
    return this.engine.activeNodeIds;
  }

  get direction() {
    return this.page.direction;
  }

  get sections() {
    return this.page.config.children;
  }

  get hasTabBar() {
    return !!this.slots["TabBar"];
  }

  get hasHeaderBar() {
    return !!this.slots["HeaderBar"];

  }

  get slots() {
    return this.page?.config?.slots || {};
  }

  @Watch("page.config", { immediate: true })
  @Watch("page.config.pos.w")
  @Watch("page.config.viewMode")
  refreshStyle() {
    const { style, viewMode, pos } = this.page.config;
    const res = cloneDeep(style) as any;
    if (viewMode === "adapt" && this.$el && this.preview) {
      const $el = this.$el;
      let realWidth = 100;
      if ($el.parentElement)
        realWidth = $el.parentElement.getBoundingClientRect().width;

      const type = (this.page as any).displayType;
      const setWidth = (pos?.w || (type.indexOf('h5') !== -1 ? 375 : 1200)) as number;

      if (setWidth && setWidth > 0) {
        const scale = realWidth / setWidth;
        res["transform"] = `scale(${scale})`;

        if (scale > 1) {
          res["transform-origin"] = `center  top`;
        } else {
          res["transform-origin"] = `left top`;
        }
      }
    }

    const newPos = cloneDeep(pos);

    this.style = transformStyle({ ...this.page.config, pos: newPos, style: res });
  }

  handleActiveChange(active: string) {
    this.engine.activeNode([active]);
  }

  handlePageClick() {
    this.engine.resetActive();
  }

  handleKeyDown(e: any) {
    switch (e.key) {
      case "Backspace":
        if (this.preview) return;
        if (this.activeNodePosition === 'slot') {
          this.engine.deleteSlot(this.activeNodeId as string);
        } else {
          this.engine.deleteNode(this.activeNodeId as string);
        }
        return;
      case "ArrowLeft":
        if (!this.activatedNode || this.activeNodePosition !== 'node') return;
        e.preventDefault();
        return this.engine.updateNodeByKey("pos.x", get(this.activatedNode, "pos.x") - 1);
      case "ArrowRight":
        if (!this.activatedNode || this.activeNodePosition !== 'node') return;
        e.preventDefault();
        return this.engine.updateNodeByKey("pos.x", get(this.activatedNode, "pos.x") + 1);
      case "ArrowUp":
        if (!this.activatedNode || this.activeNodePosition !== 'node') return;
        e.preventDefault();
        return this.engine.updateNodeByKey("pos.y", get(this.activatedNode, "pos.y") - 1);
      case "ArrowDown":
        if (!this.activatedNode || this.activeNodePosition !== 'node') return;
        e.preventDefault();
        return this.engine.updateNodeByKey("pos.y", get(this.activatedNode, "pos.y") + 1);
    }
  }

  beforeMount() {
    this.engine.changeSetting(null, this.editorSetting);
  }

  mounted() {
    window.addEventListener("keydown", this.handleKeyDown);
    this.refreshStyle();
    this.engine.load(this.page, this.setting);
    addListener((this as any).$el, this.refreshStyle);
  }

  beforeDestroy() {
    window.removeEventListener("keydown", this.handleKeyDown);
    removeListener((this as any).$el, this.refreshStyle);
  }
}
</script>

<style lang="scss" scoped>

.page-canvas-container {
  width: 100%;
  display: flex;
  flex: 1;
  height: 100%;
  overflow: auto;

  &.tab-bar-page {
    margin-bottom: 50px;
  }

  &.header-bar-page {
    margin-top: 50px;
  }
}

.editor-page-canvas {
  // display: flex;
  flex-direction: column;
  margin: 0 auto;
  box-shadow: 0 2px 4px 0 rgba(0, 0, 0, 0.12), 0 0 6px 0 rgba(0, 0, 0, 0.04);
  transform-origin: center top;
  margin-bottom: 20px;
  position: relative;

  &::-webkit-scrollbar {
    display: block;
  }

  &.column-side {
    overflow-x: hidden;
  }

  &.row-side {
    overflow-y: hidden;
  }

  .section {
    min-height: 300px;
    background-color: white;
  }

  .section-add {
    border: 2px dashed $secondColor;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 300px;
  }
}
</style>
