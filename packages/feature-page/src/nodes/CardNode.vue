<template>
  <BaseNode
    v-bind="$attrs"
    v-on="$listeners"
    :node="node"
    :sectionId="sectionId"
    :preview="preview"
    class="button-node"
  >
    <el-card class="node-main">
      <div slot="header" class="clearfix">
        <span>{{ nodeData.title }}</span>
      </div>
      <div class="card-content">
        {{ nodeData.content }}
      </div>
    </el-card>
  </BaseNode>
</template>
<style lang="scss" scoped>
@import "./node.scss";
</style>
<script lang="ts">
import { Component } from "vue-property-decorator";
import BaseNode from "./BaseNode.vue";
import NodeClass from "./NodeClass";
import { FreeNodeData, getBaseNode, IBaseNode } from "@tefact/core";
import { PageProperties } from "../config";

@Component({
  components: { BaseNode },
})
export default class CardNode extends NodeClass<IBaseNode> {
  editor: any = null;

  static DEFAULT = {
    ...getBaseNode(),
    type: "CardNode",
    data: {
      title: "卡片标题",
      content: "卡片内容",
    } as FreeNodeData,
  } as IBaseNode;

  static NODE = {
    icon: "tf-icon-card",
    type: "CardNode",
    title: "卡片",
    nodeData: CardNode.DEFAULT,
  };

  static PROPERTIES = PageProperties.defaultProperties("卡片配置", [
    {
      type: "RowsProperties",
      params: {
        title: "卡片内容设置",
        rows: [
          {
            type: "TextRow",
            params: {
              title: "标题",
              path: "data.title",
            },
          },
          {
            type: "TextAreaRow",
            params: {
              title: "内容",
              path: "data.content",
            },
          },
        ],
      },
    },
  ]);
}
</script>
