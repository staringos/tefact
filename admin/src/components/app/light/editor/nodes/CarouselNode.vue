<template>
  <BaseNode
    v-bind="$attrs"
    v-on="$listeners"
    :node="node"
    :sectionId="sectionId"
    :preview="preview"
    class="button-node"
  >
    <el-carousel class="node-main" indicator-position="outside">
      <el-carousel-item class="carousel-image-item" v-for="(item, key) in nodeData.list" :key="key">
        <img class="carousel-image" :src="item.image" />
        <div class="carousel-content">
          <h3>{{ item.title }}</h3>
          <p>{{ item.desc }}</p>
        </div>
      </el-carousel-item>
    </el-carousel>
  </BaseNode>
</template>
<style lang="scss" scoped>
@import "./node.scss";

.node-main {
  position: relative;

  .carousel-image {
    width: 100%;
    height: 100%;
    display: table-cell;
    vertical-align: middle;
  }

  ::v-deep .el-carousel__container {
    width: 100%;
    height: 100%;
  }

  .carousel-image-item, .carousel-image {
    max-width: 100%;
    max-height: 100%;
  }

  .carousel-content {
    position: absolute;
    bottom: 0;
    width: 100%;
    text-align: center;
  }
}
</style>
<script lang="ts">
import { Component, namespace } from 'nuxt-property-decorator'
import BaseNode from './BaseNode.vue'
import NodeClass from "~/components/app/light/editor/nodes/NodeClass";
import { ButtonNodeModel } from "~/utils/entities/editor/node"

const editor = namespace('editor')
const system = namespace('system')

@Component({
  components: { BaseNode }
})
export default class ImageNode extends NodeClass<ButtonNodeModel> {
  editor: any = null

  @system.Getter uploadUrl
  @editor.Action modifyNode
}
</script>
