<template>
  <div class="editor-toolbar">
    <i class="el-icon-arrow-left" @click="handleGoBack"></i>
    <div class="page-title" @click="handleOpenModify">
      {{ target.title }}
      <i class="el-icon-edit"></i>
    </div>

    <div class="tool-list">
      <el-button
        type="info"
        icon="el-icon-receiving"
        size="small"
        @click="handleSavePage"
        >保存</el-button
      >
      <el-button
        type="info"
        icon="el-icon-data-analysis"
        size="small"
        @click="handlePreviewer"
        >预览</el-button
      >
      <SharePageEditor :page="target" :pageType="featureType">
        <el-button type="info" icon="el-icon-share" size="small"
          >分享</el-button
        >
      </SharePageEditor>
    </div>

    <div class="right-button">
      <el-button
        :type="setting.grid ? 'primary' : 'default'"
        size="mini"
        @click="handleSettingChange('grid', !setting.grid)"
        v-if="featureType === 'page'"
      >
        <i :class="`tefact-icon tf-icon-grid-line`"></i>
      </el-button>

      <el-button-group size="mini">
        <el-button
          v-for="(device, i) in deviceList"
          :key="i"
          :type="engine.setting.device === device.value ? 'primary' : 'default'"
          size="mini"
          @click="handleSelectDevices(device.value)"
        >
          <i :class="`tefact-icon ${device.icon}`"></i>
        </el-button>
      </el-button-group>
    </div>
    <Previewer
      :page="target"
      :isForm="engine.isForm"
      :show="showPreviewer"
      @submit="setting.onFormDataSubmit"
      @cancel="handlePreviewerHide"
    />
  </div>
</template>
<style lang="scss"></style>
<script lang="ts">
import { Component, Prop } from "vue-property-decorator";
import SharePageEditor from "TEFACT_EDITOR/components/common/SharePageEditor.vue";
import Previewer from "TEFACT_EDITOR/components/common/Previewer.vue";
import { BaseView, DeviceType } from "@tefact/core";
import type { ITarget } from "@tefact/core";

@Component({
  components: { Previewer, SharePageEditor },
})
export default class Toolbar extends BaseView {
  @Prop() target?: ITarget;

  showPreviewer = false;
  appId: string | null = null;
  dialogVisible = false;

  deviceList = [
    { icon: "tf-icon-pc", name: "PC", value: "pc" },
    { icon: "tf-icon-mobile-phone", name: "Mobile", value: "mobile" },
  ];

  get featureType() {
    return this.engine.featureType;
  }

  handleSavePage() {
    this.engine.save();
  }

  handlePreviewer(): void {
    this.showPreviewer = true;
  }

  handlePreviewerHide() {
    this.showPreviewer = false;
  }

  handleOpenModify() {
    return this.engine.openModify();
  }

  handleGoBack() {
    return this.engine.back();
  }

  handleSelectDevices(device: DeviceType) {
    this.engine.changeSettingItem("device", device);
  }

  handleSettingChange(key: string, value: any) {
    this.engine.changeSettingItem(key, value);
  }
}
</script>
<style lang="scss">
.editor-toolbar {
  display: flex;
  align-items: center;

  .el-icon-arrow-left {
    cursor: pointer;

    &:hover {
      color: $editor-main-color;
    }
  }

  .page-title {
    margin: 0 10px;
    cursor: pointer;

    &:hover {
      color: $editor-main-color;
    }
  }

  .tool-list {
    flex: 1;
    display: flex;
    justify-content: center;

    .el-button {
      border: 0;
      background: none;
      color: $editor-text-color;

      &:hover {
        color: $editor-text-active-color;
      }
    }
  }

  .right-button {
    float: right;
    display: flex;
    justify-content: center;
    align-items: center;

    button {
      margin-right: 5px;
    }
  }
}

.editor-toolbar {
  height: 32px;
  padding: 10px;
  background-color: white;
  box-shadow: 0 2px 4px 0 rgba(0, 0, 0, 0.12), 0 0 6px 0 rgba(0, 0, 0, 0.04);
  border-bottom: 1px solid $borderSecondColor;
}
</style>
