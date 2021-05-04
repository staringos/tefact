<template>
  <div class="left-area">
    <el-tabs class="tabs" v-model="activeModel" tab-position="left" type="border-card" style="height: 200px;">
      <el-tab-pane label="零件"></el-tab-pane>
      <el-tab-pane label="页面"></el-tab-pane>
      <el-tab-pane label="资源"></el-tab-pane>
      <el-tab-pane label="JSON"></el-tab-pane>
    </el-tabs>
    <div class="left-area-content" v-show="!isCollapse">
      <NodesBar v-if="activeModel === '0'" :editorType="editorType" />
      <PagePanel v-if="activeModel === '1'" :editorType="editorType" />
      <FileListPanel v-if="activeModel === '2'" :editorType="editorType" />
      <ConfigPreviewPanel v-if="activeModel === '3'" :editorType="editorType" />
    </div>
    <CollapseButton v-model="isCollapse" />
  </div>
</template>
<script lang="ts">
import { Vue, Component, Prop } from "vue-property-decorator";
import NodesBar from "TEFACT_EDITOR/components/NodesBar.vue";
import { CollapseButton } from "@tefact/ui";
import PagePanel from "TEFACT_EDITOR/components/panels/PagePanel.vue";
import ConfigPreviewPanel from "TEFACT_EDITOR/components/panels/ConfigPreviewPanel.vue";
import FileListPanel from "TEFACT_EDITOR/components/panels/FileListPanel.vue";

@Component({
  components: { FileListPanel, ConfigPreviewPanel, PagePanel, NodesBar, CollapseButton }
})
export default class LeftArea extends Vue {
  @Prop() editorType;

  activeModel = "0";
  isCollapse = false;
}
</script>
<style lang="scss" scoped>
.left-area {
  display: flex;
  height: 100% !important;
  flex: 1;
  width: 190px;
  max-width: 193px;

  .tabs {
    width: 30px;
    max-width: 30px;
    height: 100% !important;
    background: white;
    border-top: 0;

    ::v-deep.el-tabs__header {
      width: 100%;
    }

    ::v-deep.el-tabs__item {
      height: 80px;
      writing-mode: vertical-rl;
      padding-left: 0;
      width: 30px;
      padding-right: 0px;
      display: flex;
      justify-content: center;
      align-items: center;
    }
  }

  .left-area-content {
    display: flex;
    flex: 1;
    height: 100%;
    width: 160px;
  }
}
</style>
