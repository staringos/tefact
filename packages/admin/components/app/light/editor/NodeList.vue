<template>
  <div class="editor-node-list-wrapper">

    <div class="editor-node-list">
      <div class="node-item" v-for="(node, i) in nodeList" :key="i">
      <i :class="`tefact-icon ${node.icon}`"></i>
      <span>{{node.title}}</span>
      </div>
    </div>
  </div>
</template>
<style lang="scss">

</style>
<script lang="ts">
  import { Vue, Component } from 'nuxt-property-decorator'

  @Component
  export default class AppItem extends Vue {
    nodeList = [{
        icon: 'tf-icon-Text',
        type: 'text',
        title: '文字'
    }, {
        icon: 'tf-icon-image',
        type: 'image',
        title: '图片'
    }, {
        icon: 'tf-icon-code',
        type: 'html',
        title: 'HTML'
    }, {
        icon: 'tf-icon-integral',
        type: 'div',
        title: '层'
    }, {
        icon: 'tf-icon-nav-list',
        type: 'list',
        title: '列表'
    }, {
        icon: 'tf-icon-mtbutton',
        type: 'button',
        title: '按钮'
    }]
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
