<template>
  <div class="form-node-wrapper">
    <el-upload
      ref="uploader"
      class="uploader"
      :action="setting.uploadUrl"
      :headers="setting.moreHeader"
      :show-file-list="false"
      :on-success="handleUpdate"
      drag
    >
      <img v-if="tmpInput" :src="tmpInput" class="image-node-image" />

      <i
        :class="`el-icon-upload uploader-icon ${
          tmpInput ? '' : 'show-wrapper'
        }`"
      ></i>
    </el-upload>
  </div>
</template>
<style lang="scss" scoped>
@import "./style.scss";

.uploader {
  width: 150px;
  height: 150px;
}

::v-deep .el-upload {
  width: 150px;
  height: 150px;
}

::v-deep .image-node-image,
::v-deep .el-upload-dragger {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;

  .el-icon-upload {
    font-size: 52px;
    margin: 0;
  }
}
</style>
<script lang="ts">
import { Component } from "vue-property-decorator";
import mixin from "./mixin";
import { FormProperties } from "../config";
import { BaseView } from "@tefact/core";

@Component({
  mixins: [mixin],
})
export default class InputNode extends BaseView {
  static PROPERTIES = {
    title: "图片配置",
    hasTab: true,
    tabs: [FormProperties.defaultProperties("TextRow")],
  };

  static DEFAULT = FormProperties.getBaseFormSection("ImageNode", null, 230);

  static NODE = {
    icon: "tf-icon-image",
    type: "ImageNode",
    title: "上传图片",
    nodeData: InputNode.DEFAULT,
  };

  handleUpdate(e: Array<string>) {
    (this as any).tmpInput = "https://" + e[0];
  }
}
</script>
