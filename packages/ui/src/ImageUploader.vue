<template>
  <el-upload
    ref="uploader"
    class="image-uploader"
    :action="setting.uploadUrl"
    :headers="setting.customHeader"
    :show-file-list="false"
    :on-success="handleUpdate"
    drag
  >
    <img v-if="value" :src="value" class="image-node-image" />

    <i class="el-icon-plus avatar-uploader-icon" v-if="!value"></i>
  </el-upload>
</template>
<style lang="scss" scoped>
.image-uploader {
  width: 120px;
  height: 120px;

  ::v-deep.el-upload,
  ::v-deep.el-upload--text {
    width: 120px;
    height: 120px;

    .el-upload-dragger {
      width: 120px;
      height: 120px;
      display: flex;
      align-items: center;
      justify-content: center;
    }
  }

  .image-node-image {
    background-size: 100% 100%;
    width: 120px;
  }
}
</style>
<script lang="ts">
import { Component, Prop } from "vue-property-decorator";
import { BaseView } from "@tefact/core";

@Component
export default class ImageUploader extends BaseView {
  @Prop() value!: string;

  handleUpdate(e: Array<string>): void {
    this.$emit("input", `https://${e[0]}`);
  }
}
</script>
