<template>
  <BaseNode
    v-bind="$attrs"
    v-on="$listeners"
    :node="node"
    :sectionId="sectionId"
    class="image-node"
  >
    <el-upload
      ref="uploader"
      class="uploader"
      :action="uploadUrl"
      :show-file-list="false"
      :on-success="handleUpdate"
      drag
    >
      <img
        v-if="imageData.url"
        :src="imageData.url"
        class="image-node-image"
        :alt="imageData.title">

      <i :class="`el-icon-upload uploader-icon ${imageData.url ? '' : 'show-wrapper'}`"></i>
    </el-upload>

    <div
      :class="`uploader-icon-wrapper ${imageData.url ? '' : 'show-wrapper'}`"
    ></div>
  </BaseNode>
</template>
<style lang="scss" scoped>
  @import "../../../../../assets/styles/variables";

  .image-node {
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: $gray-01;
    position: relative;

    &, .uploader, /deep/ .el-upload, /deep/ .el-upload-dragger {
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

    /deep/ .image-node-image {
      width: 100%;
      height: 100%;
    }

    &:hover {
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
  import { Component, namespace } from 'nuxt-property-decorator'
  import { cloneDeep } from 'lodash'
  import { ImageNodeModel } from '~/utils/entities/editor/node'
  import BaseNode from './BaseNode.vue'
  import NodeClass from "~/components/app/light/editor/nodes/NodeClass";

  const editor = namespace('editor')
  const system = namespace('system')

  @Component({
    components: { BaseNode }
  })
  export default class ImageNode extends NodeClass<ImageNodeModel> {
    editor: any = null

    @system.Getter uploadUrl
    @editor.Action modifyNode

    get imageData() {
      return this.node?.data
    }

    handleToUpdate(e) {
      this.$emit('click', e);
    }

    handleUpdate(e) {
      const node = cloneDeep(this.node);
      (node.data as any).url = 'http://' + e[0]
      this.modifyNode({ sectionId: this.sectionId, node })
    }
  }
</script>
