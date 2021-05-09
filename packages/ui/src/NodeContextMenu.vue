<template>
  <el-menu
    default-active="2"
    class="node-context-menu"
    v-show="visible"
    :style="style"
  >
    <el-menu-item
      index="2"
      v-for="(menu, i) in options"
      @click="menu.onClick"
      :key="i"
    >
      <i :class="menu.icon"></i>
      <span slot="title">{{ menu.name }}</span>
    </el-menu-item>
    <WidgetDialog
      v-model="isWidgetDialogShow"
      :nodeId="nodeId"
    />
  </el-menu>
</template>
<script lang="ts">
import { Component, Prop, Watch } from "vue-property-decorator";
import { BaseView } from "@tefact/core";
import type { IPosition } from "@tefact/core";
import WidgetDialog from "./WidgetDialog.vue";

// const editor = namespace("editor");

@Component({
  components: {
    WidgetDialog
  }
})
export default class NodeContextMenu extends BaseView {
  @Prop(Boolean) visible!: boolean;
  @Prop(String) nodeId!: string;
  @Prop(String) sectionId!: string;
  @Prop() pos!: IPosition;

  isWidgetDialogShow = false;

  // @editor.Action deleteNode
  // @editor.Action copyNode
  // @editor.Action reOrderNode

  get options() {
    return [
      {
        name: "置顶",
        icon: "tefact-icon tf-icon-vertical-align-top",
        class: "",
        type: "top",
        onClick: () => {
          this.engine.reOrderNode(this.nodeId, this.sectionId, "top");
          this.$emit("hide");
        },
      },
      {
        name: "置底",
        icon: "tefact-icon tf-icon-vertical-align-bottom",
        class: "",
        type: "bottom",
        onClick: () => {
          this.engine.reOrderNode(this.nodeId, this.sectionId, "bottom");
          this.$emit("hide");
        },
      },
      {
        name: "上移一个",
        icon: "tefact-icon el-icon-top",
        class: "",
        type: "up",
        onClick: () => {
          this.engine.reOrderNode(this.nodeId, this.sectionId, "up");
          this.$emit("hide");
        },
      },
      {
        name: "下移一个",
        icon: "tefact-icon el-icon-bottom",
        class: "",
        type: "down",
        onClick: () => {
          this.engine.reOrderNode(this.nodeId, this.sectionId, "down");
          this.$emit("hide");
        },
      },
      {
        name: "复制",
        icon: "tefact-icon tf-icon-clipboard",
        class: "",
        type: "copy",
        onClick: () => {
          this.engine.copyNode(this.nodeId);
          this.$emit("hide");
        },
      },
      {
        name: "生成组件",
        icon: "el-icon-box",
        class: "",
        type: "copy",
        onClick: () => {
          this.isWidgetDialogShow = true;
          this.$emit("hide");
        },
      },
      {
        name: "删除",
        icon: "el-icon-delete",
        class: "el-icon-delete",
        type: "delete",
        onClick: () => {
          this.engine.deleteNode(this.nodeId);
          this.$emit("hide");
        },
      },
    ];
  }

  get style() {
    if (!this.pos) return null;
    return {
      left: this.pos.x + "px",
      top: this.pos.y + "px",
    };
  }

  @Watch("visible")
  handleVisibleChange() {
    if (this.visible) {
      window.addEventListener("click", this.handleHide);
    } else {
      window.removeEventListener("click", this.handleHide);
    }
  }

  handleHide() {
    this.$emit("hide");
  }
}
</script>
<style lang="scss" scoped>
.node-context-menu {
  position: fixed;
  background: #fff;
  z-index: 999;
  border: 1px solid #eee;
  box-shadow: 0 0.5em 1em 0 rgba(0, 0, 0, 0.1);
  border-radius: 1px;
  width: 180px;
}
</style>
