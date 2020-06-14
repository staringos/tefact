<template>
  <BaseNode
    v-bind="$attrs"
    v-on="$listeners"
    :node="node"
    :sectionId="sectionId"
    class="text-node"
  >
    <editor-content
      v-if="editor"
      spellcheck="false"
      :editor="editor"
      ref="editor"
      class="text-node-editor"
    />
    <div class="mask" v-if="!editing" @dblclick="handleEditing"></div>
  </BaseNode>
</template>
<style lang="scss" scoped>
  /deep/ .text-node-editor, /deep/ .ProseMirror {
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
  }
</style>
<script lang="ts">
  import { Vue, Component, Prop, namespace } from 'nuxt-property-decorator'
  import _ from 'lodash'
  import NodeClass from './NodeClass'
  import { TextNodeModel } from '~/utils/entities/editor/node'
  import BaseNode from './BaseNode.vue'
  import { Editor, EditorContent } from "tiptap";
  import { Bold, Italic, Strike, Underline } from "tiptap-extensions";

  const editor = namespace('editor')

  @Component({
    components: { BaseNode, EditorContent }
  })
  export default class TextNode extends NodeClass {
    @Prop() node!: TextNodeModel
    @Prop() preview!: boolean
    @Prop() sectionId!: string

    editor: any = null
    editing: boolean = false

    @editor.Action modifyNode

    init () {
      const editor = new Editor({
        extensions: [
          new Bold(),
          new Italic(),
          new Strike(),
          new Underline()
        ],
        editable: !this.preview,
        content: this.node.data.text
      });

      // this.editor.on('update', this.handleUpdate)
      editor.on('blur', this.handleUpdate)

      this.editor = editor
    }

    handleEditing() {
      this.editing = true
      this.editor.focus()
    }

    handleUpdate() {
      const newContent = this.editor.getHTML()
      const node = _.cloneDeep(this.node)
      node.data.text = newContent
      this.modifyNode({ sectionId: this.sectionId, node })

      this.editing = false
    }

    mounted() {
      this.init()
    }
  }
</script>
