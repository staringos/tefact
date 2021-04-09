<template>
  <BaseRow :title="title" v-bind="$attrs">
    <el-upload
      ref="uploader"
      class="uploader"
      :action="setting.uploadUrl"
      :headers="setting.customHeader"
      :show-file-list="false"
      :on-success="handleUpdate"
      drag
    >
      <img v-if="tmpText" :src="tmpText" class="image-node-image" />
      <i
        v-else
        :class="`el-icon-upload uploader-icon ${tmpText ? '' : 'show-wrapper'}`"
      ></i>
    </el-upload>
  </BaseRow>
</template>
<style lang="scss" scoped>
.uploader,
::v-deep .image-node-image,
::v-deep .el-upload,
::v-deep .el-upload-dragger {
  width: 120px;
  height: 120px;
}
</style>
<script lang="ts">
import { Component } from "vue-property-decorator";
import BaseRow from "./BaseRow.vue";
import RowMixin from "./RowMixin";
import { BaseView } from "@tefact/core";

@Component({
  components: { BaseRow },
  mixins: [RowMixin],
})
export default class ImageUploadRow extends BaseView {
  handleUpdate(e: Array<string>) {
    (this as any).handleChange("https://" + e[0]);
  }
}
</script>
