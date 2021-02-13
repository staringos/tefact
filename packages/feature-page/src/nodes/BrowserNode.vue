<template>
  <BaseNode
    v-bind="$attrs"
    v-on="$listeners"
    :node="node"
    :sectionId="sectionId"
    :preview="preview"
    class="browser-node"
  >
    <iframe class="node-main" :src="nodeData.src"></iframe>
    <div class="musk" v-if="!preview" @dblclick="noticeCannotClick"></div>
  </BaseNode>
</template>
<style lang="scss" scoped>
@import "./node.scss";
.browser-node {
  position: relative;
  .musk {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: transparent;
    z-index: 999;
  }
}
.node-main {
  border: 0;
}
</style>
<script lang="ts">
import { Component } from "vue-property-decorator";
import BaseNode from "./BaseNode.vue";
import NodeClass from "./NodeClass";
import { getBaseNode, IBaseNode } from "@tefact/core";
import { PageProperties } from "../config";

@Component({
  components: { BaseNode },
})
export default class BrowserNode extends NodeClass<IBaseNode> {
  editor: any = null;

  static DEFAULT = {
    ...getBaseNode(),
    type: "BrowserNode",
    data: {
      src: "https://tefact.com",
    },
  };

  static NODE = {
    icon: "tf-icon-browser",
    type: "BrowserNode",
    title: "网页",
    nodeData: BrowserNode.DEFAULT,
  };

  static PROPERTIES = PageProperties.defaultProperties("网页配置", [
    {
      type: "RowsProperties",
      params: {
        title: "网页内容设置",
        rows: [
          {
            type: "TextRow",
            params: {
              title: "链接",
              path: "data.src",
            },
          },
        ],
      },
    },
  ]);

  noticeCannotClick() {
    (this as any).$message.warning(
      "编辑状态下，网页组件内部不可点击，发布后可正常操作!"
    );
  }
}
</script>
