<template>
  <div class="editor-wrapper">
    <div class="editor-container">
      <div class="editor-toolbar">
        <i class="el-icon-arrow-left"></i>
        <div class="page-title">
          {{page.title}}
          <i class="el-icon-edit"></i>
        </div>
      </div>
      <div class="editor-main">
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

      .editor-toolbar {
        display: flex;
        align-items: center;

        .page-title {
          margin: 0 10px;
          cursor: pointer;

          &:hover {
            color: $editor-main-color;
          }
        }
      }

      .editor-toolbar {
        height: 32px;
        padding: 10px;
        background-color: white;
        box-shadow: 0 2px 4px 0 rgba(0,0,0,.12), 0 0 6px 0 rgba(0,0,0,.04);
      }

      .editor {
        flex: 1;
        overflow: auto;
      }

      .editor-main {
        -webkit-box-flex: 1;
        flex-grow: 1;
        display: flex;
        overflow: auto;
        flex-direction: column;
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

  @Component({
    layout: 'UserAdmin',
    components: { Canvas }
  })
  export default class EditorPage extends Vue {
    page = {
      title: '这是一个新页面'
    }
  }
</script>
