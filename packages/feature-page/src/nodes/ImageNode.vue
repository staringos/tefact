<template>
  <BaseNode
    v-bind="$attrs"
    v-on="$listeners"
    :node="node"
    :sectionId="sectionId"
    :preview="preview"
    :class="`image-node ${preview ? 'preview' : ''}`"
  >
    <el-upload
      ref="uploader"
      class="uploader"
      v-if="!preview"
      :action="setting.uploadUrl"
      :headers="setting.customHeader"
      :show-file-list="false"
      :on-success="handleUpdate"
      drag
    >
      <img
        v-if="imageData.url"
        :src="imageData.url"
        class="image-node-image"
        :alt="imageData.title"
      />

      <i
        :class="`el-icon-upload uploader-icon ${
          imageData.url ? '' : 'show-wrapper'
        }`"
      ></i>
    </el-upload>

    <div
      :class="`uploader-icon-wrapper ${imageData.url ? '' : 'show-wrapper'}`"
      v-if="!preview"
    ></div>
    <img
      v-if="preview && imageData.url"
      :src="imageData.url"
      class="image-node-image"
      :alt="imageData.title"
    />
  </BaseNode>
</template>
<style lang="scss" scoped>
.image-node {
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: $gray-01;
  position: relative;

  &,
  .uploader,
  ::v-deep .el-upload,
  ::v-deep .el-upload-dragger {
    width: 100%;
    height: 100%;
  }

  .uploader {
    display: flex;
    justify-content: center;
  }

  .uploader-icon-wrapper {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    display: none;
    justify-content: center;
    align-items: center;
    background: $gray-01;
    opacity: 30%;
  }

  .uploader-icon {
    display: none;
    font-weight: bold;
    font-size: 32px;
    text-align: center;
    color: $mainColor;
    z-index: 1000;
    position: absolute;
    top: 50%;
    left: 50%;
    width: 32px;
    height: 32px;
    line-height: 32px;
    margin-left: -16px;
    margin-top: -16px;
  }

  ::v-deep .image-node-image {
    width: 100%;
    height: 100%;
  }

  &:not(.preview):hover {
    .uploader-icon-wrapper {
      display: flex;
    }

    .uploader-icon {
      display: block;
    }
  }

  .show-wrapper {
    display: flex;
  }
}
</style>
<script lang="ts">
import { Component } from "vue-property-decorator";
import cloneDeep from "lodash/cloneDeep";
import BaseNode from "./BaseNode.vue";
import NodeClass from "./NodeClass";
import { FreeNodeData, getBaseNode } from "@tefact/core";
import type { IBaseNode } from "@tefact/core";
import { PageProperties } from "../config";

// const editor = namespace("editor");
// const system = namespace("system");
// const user = namespace("user");

@Component({
  components: { BaseNode },
})
export default class ImageNode extends NodeClass<IBaseNode> {
  editor: any = null;

  // @system.Getter uploadUrl;
  // @user.Getter authHeader;
  // @editor.Action modifyNode;

  get imageData() {
    return this.node?.data;
  }

  handleToUpdate(e: any) {
    this.$emit("click", e);
  }

  handleUpdate(e: Array<string>) {
    console.log("success:", e);
    const node = cloneDeep(this.node);
    (node.data as any).url = "https://" + e[0];
    this.engine.updateNode(node);
  }

  static DEFAULT = {
    ...getBaseNode(),
    type: "ImageNode",
    data: {
      url: null,
      title: "",
    } as FreeNodeData,
  } as IBaseNode;

  static NODE = {
    icon: "tf-icon-image",
    type: "image",
    title: "图片",
    nodeData: ImageNode.DEFAULT,
  };

  static PROPERTIES = PageProperties.defaultProperties("图片配置");
}
</script>
