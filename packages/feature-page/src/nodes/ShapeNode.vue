<template>
  <BaseNode
    v-bind="$attrs"
    v-on="$listeners"
    :node="node"
    :sectionId="sectionId"
    :preview="preview"
    :isShape="true"
    class="text-node"
  >
    <component :node="node" :is="node.data.target"></component>
  </BaseNode>
</template>
<style lang="scss" scoped>
::v-deep .text-node-editor,
::v-deep .ProseMirror,
.editor-content {
  width: 100%;
  height: 100%;
}

.text-node {
  .mask {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
  }

  .editor-content {
    display: flex;
    flex: 1;
  }
}
</style>
<script lang="ts">
import { Component, Prop } from "vue-property-decorator";
import NodeClass from "./NodeClass";
import BaseNode from "./BaseNode.vue";
import shapes from "../shapes";
import { getBaseNode } from "@tefact/core";
import type { IBaseNode } from "@tefact/core";
import { PageProperties } from "../config";

// const editor = namespace("editor");

@Component({
  components: { BaseNode, ...shapes },
})
export default class ShapeNode extends NodeClass<IBaseNode> {
  @Prop() node!: IBaseNode;
  @Prop() preview!: boolean;
  @Prop() sectionId!: string;

  editor: any = null;
  editing = false;

  static DEFAULT = {
    ...getBaseNode(50, 50, "tefact-icon tf-icon-star"),
    type: "ShapeNode",
    data: {},
  } as IBaseNode;

  static NODE = {
    icon: "tf-icon-shapes",
    type: "text",
    title: "图形",
    nodeData: ShapeNode.DEFAULT,
  };

  static PROPERTIES = PageProperties.defaultProperties("图形配置");
}
</script>
