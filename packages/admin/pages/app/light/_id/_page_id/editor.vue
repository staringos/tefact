<template>
  <div class="editor-wrapper">
    <div class="editor-container">
      <Toolbar :page="page" :editorSetting="editorSetting"></Toolbar>
        <div class="editor-main">
          <NodeList />
          <Canvas />
        </div>
    </div>
    <div class="editor-side-bar">
      <el-tabs type="border-card">
        <el-tab-pane label="基本信息"></el-tab-pane>
        <el-tab-pane label="数据展示"></el-tab-pane>
        <el-tab-pane label="样式"></el-tab-pane>
      </el-tabs>
    </div>
  </div>
</template>
<style lang="scss" scoped>
  @import "../../../../../assets/styles/variables";

  .editor-wrapper {
    display: flex;
    flex: 1;
    overflow: hidden;

    .editor-container {
      background: #f0f2f5;
      flex: 3;
      display: flex;
      flex-direction: column;

      .editor {
        flex: 1;
        overflow: auto;
      }

      .editor-main {
        -webkit-box-flex: 1;
        flex-grow: 1;
        display: flex;
        overflow: auto;
        flex-direction: row;
        padding: 20px 20px 20px 20px;
      }
    }
    .editor-side-bar {
      flex: 1;
      background: white;
      display: flex;

      /deep/ .el-tabs {
        flex: 1;
        box-shadow: none;
        margin-top: -1px;
      }
    }
  }
</style>
<script lang="ts">
  import { Vue, Component } from 'nuxt-property-decorator'
  import Canvas from '~/components/app/light/editor/Canvas.vue'
  import Toolbar from '~/components/app/light/editor/Toolbar.vue'
  import NodeList from '~/components/app/light/editor/NodeList.vue';

  @Component({
    layout: 'UserAdmin',
    components: {NodeList, Canvas, Toolbar }
  })
  export default class EditorPage extends Vue {
    page = {
      title: '这是一个新页面'
    }

    editorSetting = {
      device: 'pc',
    }
  }
</script>
