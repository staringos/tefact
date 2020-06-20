<template>
  <div class="editor-node-list-wrapper">

    <div class="editor-node-list">
      <div class="node-item" v-for="(node, i) in nodeList" :key="i" @click="handleAddNode(node.nodeData)">
        <i :class="`tefact-icon ${node.icon}`"></i>
        <span>{{node.title}}</span>
      </div>
    </div>
  </div>
</template>
<style lang="scss">
  .editor-node-list-wrapper {
    position: fixed;
  }
</style>
<script lang="ts">
  import { Vue, Component, namespace } from 'nuxt-property-decorator'
  import { NodeListConstants } from '~/utils/constants/Editor'
  import { cloneDeep } from 'lodash-es'

  const editor = namespace('editor')

  @Component
  export default class NodeList extends Vue {
    nodeList = NodeListConstants

    @editor.Action addNode

    handleAddNode(nodeData) {
      this.addNode(cloneDeep(nodeData))
    }
  }
</script>
<style lang="scss">
  @import "../../../../assets/styles/variables";

  .editor-node-list-wrapper {
    overflow: auto;
    width: 100px;
    background: #fff;

    .editor-node-list {
      display: flex;
      flex-direction: column;
      padding: 10px;

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

        &:hover {
          color: $secondColor;
          border: 1px solid $editor-node-border-color;
        }
      }
    }
  }
</style>
