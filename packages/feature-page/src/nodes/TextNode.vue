<template>
  <BaseNode
    v-bind="$attrs"
    v-on="$listeners"
    :node="node"
    :sectionId="sectionId"
    :preview="preview"
    class="text-node"
  >
    <div
      class="editor-content"
      :style="textContextStyle"
      v-html="node.data.target"
      :contenteditable="editing"
      ref="editor"
      @keydown="handleKeydown"
      @blur="handleUpdate"
    ></div>
    <div class="mask" v-if="!editing" @dblclick="handleEditing"></div>
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
import cloneDeep from "lodash/cloneDeep";
import NodeClass from "./NodeClass";
import BaseNode from "./BaseNode.vue";
import { FreeNodeData, getBaseNode, IBaseNode } from "@tefact/core";
import { PageProperties } from "../config";

@Component({
  components: { BaseNode },
})
export default class TextNode extends NodeClass<IBaseNode> {
  @Prop() node!: IBaseNode;
  @Prop() preview!: boolean;
  @Prop() sectionId!: string;

  editor: any = null;
  editing = false;

  get textContextStyle() {
    const { style } = this.node;
    return {
      // ...transformStyle(this.node),
      "justify-content": style["justify-content"],
      "align-items": style["align-items"],
    };
  }

  handleKeydown(e: Event) {
    if (this.editing) e.stopPropagation();
  }

  handleEditing() {
    this.editing = true;
    if (this.editing) {
      this.$nextTick(() => {
        (this.$refs.editor as HTMLDivElement).focus();
      });
    }
  }

  handleUpdate() {
    const newContent = (this.$refs.editor as any).innerHTML;
    const node = cloneDeep(this.node);
    node.data.target = newContent;
    this.engine.updateNode(node);
    this.editing = false;
  }

  static DEFAULT = {
    ...getBaseNode(),
    type: "TextNode",
    data: {
      target: "请输入文字",
    } as FreeNodeData,
  } as IBaseNode;

  static NODE = {
    icon: "tf-icon-Text",
    type: "text",
    title: "文字",
    nodeData: TextNode.DEFAULT,
  };

  static PROPERTIES = PageProperties.defaultProperties("文字元素配置");
}
</script>
