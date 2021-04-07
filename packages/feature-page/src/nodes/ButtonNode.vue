<template>
  <BaseNode
    v-bind="$attrs"
    v-on="$listeners"
    :node="node"
    :sectionId="sectionId"
    :preview="preview"
    class="button-node"
  >
    <el-button
      class="button-node-main"
      :style="{ width: config.pos.w, height: config.pos.h, ...config.style }"
      v-bind="nodeData"
      @click="handleClick"
      >{{ nodeData.text }}</el-button
    >
  </BaseNode>
</template>
<style lang="scss" scoped>
.button-node {
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: $gray-01;
  position: relative;

  .button-node-main {
    width: 100%;
    height: 100%;
  }
}
</style>
<script lang="ts">
import { Component } from "vue-property-decorator";
import BaseNode from "./BaseNode.vue";
import NodeClass from "./NodeClass";
import { FreeNodeData, getBaseNode } from "@tefact/core";
import type { IBaseNode } from "@tefact/core";
import { PageProperties } from "../config";

@Component({
  components: { BaseNode },
})
export default class ButtonNode extends NodeClass<IBaseNode> {
  editor: any = null;

  handleClick() {
    if (this.nodeData.link) {
      location.href = this.nodeData.link;
    }
  }

  static DEFAULT = {
    ...getBaseNode(98, 40),
    type: "ButtonNode",
    data: {
      text: "按钮",
      type: "primary",
    } as FreeNodeData,
  } as IBaseNode;

  static NODE = {
    icon: "tf-icon-mtbutton",
    type: "button",
    title: "按钮",
    nodeData: ButtonNode.DEFAULT,
  };

  static PROPERTIES = PageProperties.defaultProperties("图片配置", null, [
    {
      type: "RowsProperties",
      params: {
        title: "按钮设置",
        rows: [
          {
            type: "SelectRow",
            params: {
              title: "类型",
              path: "data.type",
              selectOptions: [
                { value: "primary", label: "Primary" },
                { value: "info", label: "Info" },
                { value: "warning", label: "Warning" },
                { value: "danger", label: "Danger" },
                { value: "text", label: "Text" },
                { value: "success", label: "Success" },
              ],
            },
          },
          {
            type: "TextRow",
            params: {
              title: "按钮文字",
              path: "data.text",
            },
          },
          {
            type: "SwitchRow",
            params: {
              title: "朴素按钮",
              path: "data.plain",
            },
          },
          {
            type: "SwitchRow",
            params: {
              title: "圆角",
              path: "data.round",
            },
          },
          {
            type: "SwitchRow",
            params: {
              title: "圆形",
              path: "data.circle",
            },
          },
        ],
      },
    },
  ]);
}
</script>
