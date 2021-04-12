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
      :style="style"
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

  get style() {
    const { config } = this;
    const res = { width: config.pos.w, height: config.pos.h, ...config.style } as any;

    if (this.config.data.round) {
      delete res["border-radius"];
    }
    return res;
  }

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
                { value: "primary", label: "主要" },
                { value: "info", label: "普通" },
                { value: "warning", label: "警告" },
                { value: "danger", label: "错误" },
                { value: "text", label: "文字" },
                { value: "success", label: "成功" },
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
