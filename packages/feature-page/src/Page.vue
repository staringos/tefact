<template>
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
</template>
<script lang="ts">
import { Component, Prop, Watch } from "vue-property-decorator";
import { addListener, removeListener } from "resize-detector";

import "vue-draggable-resizable-gorkys/dist/VueDraggableResizable.css";
import PageSection from "./nodes/SectionNode.vue";
import AddButton from "./components/AddButton.vue";
import cloneDeep from "lodash/cloneDeep";
import { transformStyle } from "@tefact/utils";
import { BaseView } from "@tefact/core";
import type { ISetting, ITarget } from "@tefact/core";

@Component({
  components: {
    AddButton,
    PageSection,
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

  @Watch("page.config", { immediate: true })
  refreshStyle() {
    const { style, viewMode, pos } = this.page.config;
    const res = cloneDeep(style) as any;
    if (viewMode === "adapt" && this.$el && this.preview) {
      const $el = this.$el;
      let realWidth = 100;
      if ($el.parentElement)
        realWidth = $el.parentElement.getBoundingClientRect().width;

      const type = (this.page as any).display_type;
      const setWidth = (pos?.w || (type.indexOf('h5') !== -1 ? 375 : 1200)) as number;

      if (setWidth && setWidth > 0) {
        res["transform"] = `scale(${realWidth / setWidth})`;
      }
    }

    this.style = transformStyle({ ...this.page.config, style: res });
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
        this.engine.deleteNode(this.activeNodeId as string);
    }
  }

  beforeMount() {
    this.engine.changeSetting(null, this.editorSetting);
  }

  mounted() {
    window.addEventListener("keydown", this.handleKeyDown);
    this.refreshStyle();
    addListener((this as any).$el, this.refreshStyle);
  }

  beforeDestroy() {
    window.removeEventListener("keydown", this.handleKeyDown);
    removeListener((this as any).$el, this.refreshStyle);
  }
}
</script>

<style lang="scss" scoped>
.editor-page-canvas {
  // display: flex;
  flex-direction: column;
  margin: 0 auto;
  box-shadow: 0 2px 4px 0 rgba(0, 0, 0, 0.12), 0 0 6px 0 rgba(0, 0, 0, 0.04);
  transform-origin: center top;
  margin-bottom: 20px;

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
