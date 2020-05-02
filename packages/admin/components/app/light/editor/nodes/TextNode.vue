<template>
  <BaseNode
    v-bind="$attrs"
    v-on="$listeners"
    :node="node"
    class="text-node"
  >
    <editor-content
      v-if="editor"
      spellcheck="false"
      :editor="editor"
      ref="editor"
      class="text-node-editor"
    />
  </BaseNode>
</template>
<style lang="scss" scoped>
  /deep/ .text-node-editor, /deep/ .ProseMirror {
    width: 100%;
    height: 100%;
  }
</style>
<script lang="ts">
  import { Vue, Component, Prop } from 'nuxt-property-decorator'
  import { TextNodeModel } from '~/utils/entities/editor/node'
  import BaseNode from './BaseNode.vue'
  import { Editor, EditorContent } from "tiptap";
  import { Bold, Italic, Strike, Underline } from "tiptap-extensions";

  @Component({
    components: { BaseNode, EditorContent }
  })
  export default class TextNode extends Vue {
    @Prop() node!: TextNodeModel
    @Prop() preview!: boolean
    editor = null

    init () {
      this.editor = new Editor({
        extensions: [
          new Bold(),
          new Italic(),
          new Strike(),
          new Underline()
        ],
        editable: !this.preview,
        content: this.node.data.text
      });
    }

    mounted() {
      this.init()
    }
  }
</script>
