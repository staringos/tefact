<template>
  <BaseNode
    v-bind="$attrs"
    v-on="$listeners"
    :node="node"
    :sectionId="sectionId"
    :preview="preview"
    class="text-node"
  >
    <!--    <editor-content-->
    <!--      v-if="editor"-->
    <!--      spellcheck="false"-->
    <!--      :editor="editor"-->
    <!--      ref="editor"-->
    <!--      class="text-node-editor"-->
    <!--      @keydown.native="handleKeydown"-->
    <!--    />-->
    <div
      class="editor-content"
      :style="textContextStyle"
      v-html="node.data.text"
      :contenteditable="editing"
      ref="editor"
      @keydown="handleKeydown"
    ></div>
    <div class="mask" v-if="!editing" @dblclick="handleEditing"></div>
  </BaseNode>
</template>
<style lang="scss" scoped>
  ::v-deep .text-node-editor, ::v-deep .ProseMirror, .editor-content {
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
  import { Component, Prop, namespace } from 'nuxt-property-decorator'
  import cloneDeep from 'lodash/cloneDeep'
  import NodeClass from './NodeClass'
  import { TextNodeModel } from '~/utils/entities/editor/node'
  import BaseNode from './BaseNode.vue'

  const editor = namespace('editor')

  @Component({
    components: { BaseNode }
  })
  export default class TextNode extends NodeClass<TextNodeModel> {
    @Prop() node!: TextNodeModel
    @Prop() preview!: boolean
    @Prop() sectionId!: string

    editor: any = null
    editing: boolean = false

    @editor.Action modifyNode

    get textContextStyle() {
      const { style } = this.node.config;
      return {
        "justify-content": style["justify-content"],
        "align-items": style["align-items"]
      }
    }

    handleKeydown(e) {
      if (this.editing) e.stopPropagation()
    }

    handleEditing() {
      this.editing = true
    }

    handleUpdate() {
      const newContent = (this.$refs.editor as any).innerHTML;
      const node = cloneDeep(this.node)
      node.data.text = newContent
      this.modifyNode({ sectionId: this.sectionId, node })

      this.editing = false
    }
  }
</script>
