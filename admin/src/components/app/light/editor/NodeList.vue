<template>
  <div class="editor-node-list-wrapper" @click.stop>
    <div class="header" v-if="editorDetails.title" @back="handleGoBack">
      <span>{{editorDetails.title}}</span>
    </div>
    <div class="editor-node-list">
      <div class="node-item" v-for="(node, i) in editorDetails.list" :key="i" @click="handleAddNode(node.nodeData)">
        <i :class="`tefact-icon ${node.icon}`"></i>
        <span>{{node.title}}</span>
      </div>
    </div>
  </div>
</template>
<script lang="ts">
  import { Vue, Component, namespace, Prop } from 'nuxt-property-decorator'
  import { FormNodeList, NodeListConstants } from '~/utils/constants/Editor'
  import cloneDeep from 'lodash/cloneDeep'

  const editor = namespace('editor')

  const EditorNodesDetails = {
    form: {
      title: "表单",
      list: FormNodeList
    },
    default: {
      title: null,
      list: NodeListConstants
    }
  }

  @Component
  export default class NodeList extends Vue {
    @editor.Action addNode

    @Prop() editorType

    get editorDetails() {
      return EditorNodesDetails[this.editorType] || EditorNodesDetails.default
    }

    // get isDefault() {
    //   return this.editorType === "pc" || this.editorType === "h5"
    // }

    handleAddNode(nodeData) {
      this.addNode(cloneDeep(nodeData))
    }

    handleGoBack() {

    }
  }
</script>
<style lang="scss">
  .editor-node-list-wrapper {
    overflow: auto;
    width: 160px;
    background: #fff;
    border-right: 1px solid $borderSecondColor;

    .header {
      width: 100%;
      height: 38px;
      line-height: 38px;
      text-align: center;
      font-size: 16px;
      font-weight: normal;
      border-bottom: 1px solid $borderColor;
    }

    .editor-node-list {
      display: flex;
      flex-direction: row;
      padding: 10px;
      flex-wrap: wrap;

      .node-item {
        width: 70px;
        height: 70px;
        border-radius: 3px;
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
        cursor: pointer;
        user-select: none;
        box-sizing: border-box;

        i {
          font-size: 20px;
          color: $mainColor;
        }

        span {
          font-size: 12px;
          color: $textMainColor;
          margin-top: 5px;
        }

        &:hover {
          color: $secondColor;
          border: 1px solid $editor-node-border-color;
        }
      }
    }
  }
</style>
