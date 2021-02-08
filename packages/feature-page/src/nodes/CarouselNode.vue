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
      <el-carousel-item
        class="carousel-image-item"
        v-for="(item, key) in nodeData.list"
        :key="key"
      >
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

  .carousel-image-item,
  .carousel-image {
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
import { Component } from "vue-property-decorator";
import BaseNode from "./BaseNode.vue";
import NodeClass from "./NodeClass";
import { getBaseNode, IBaseNode } from "@tefact/core";
import { PageProperties } from "../config";

@Component({
  components: { BaseNode },
})
export default class CarouselNode extends NodeClass<IBaseNode> {
  editor: any = null;

  static DEFAULT = {
    type: "CarouselNode",
    config: getBaseNode(),
    data: {
      list: [
        {
          image: "/images/image.png",
          title: "Default Image",
          desc: "Default Image",
          link: "http://saas.tefact.com",
        },
        {
          image: "/images/image.png",
          title: "Default Image",
          desc: "Default Image",
          link: "http://saas.tefact.com",
        },
        {
          image: "/images/image.png",
          title: "Default Image",
          desc: "Default Image",
          link: "http://saas.tefact.com",
        },
      ],
    },
  };

  static NODE = {
    icon: "tf-icon-lunbotu",
    type: "CarouselNode",
    title: "轮播图",
    nodeData: CarouselNode.DEFAULT,
  };

  static PROPERTIES = PageProperties.defaultProperties("轮播图配置", [
    {
      type: "ListProperties",
      params: {
        title: "轮播图内容设置",
        path: "data.list",
        rows: [
          {
            type: "TextRow",
            params: {
              title: "标题",
              path: "title",
            },
          },
          {
            type: "TextRow",
            params: {
              title: "描述",
              path: "desc",
            },
          },
          {
            type: "TextRow",
            params: {
              title: "图片",
              path: "image",
            },
          },
          {
            type: "TextRow",
            params: {
              title: "超链接",
              path: "link",
            },
          },
        ],
      },
    },
  ]);
}
</script>
