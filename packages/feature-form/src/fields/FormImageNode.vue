<template>
  <div class="form-node-wrapper">
    <img :src="node.data ? node.data.link : ''" :style="style" />
  </div>
</template>
<style lang="scss">
@import "./style.scss";
.form-node-wrapper {
  position: relative;
  padding: 0;
}
</style>
<script lang="ts">
import { Vue, Component } from "vue-property-decorator";
import mixin from "./mixin";
import { FormProperties } from "../config";

@Component({
  mixins: [mixin],
})
export default class FormImageNode extends Vue {
  get style() {
    if (!(this as any).node.data) return {};

    const { isFullWidth, imageStyle } = (this as any).node.data;
    const res = {
      width: imageStyle?.width + "px",
      height: imageStyle?.height + "px",
    };
    if (isFullWidth) {
      res["width"] = "100%";
    }

    return res;
  }

  static PROPERTIES = {
    title: "描述配置",
    hasTab: true,
    tabs: [
      FormProperties.defaultStyledProperties(),
      {
        title: "图片",
        components: [
          {
            type: "RowsProperties",
            params: {
              title: "基本信息",
              rows: [
                {
                  type: "ImageUploadRow",
                  params: {
                    title: "图片",
                    path: "data.link",
                  },
                },
                {
                  type: "NumberRow",
                  params: {
                    title: "宽度",
                    path: "data.imageStyle.width",
                  },
                },
                {
                  type: "NumberRow",
                  params: {
                    title: "高度",
                    path: "data.imageStyle.height",
                  },
                },
                {
                  type: "SwitchRow",
                  params: {
                    title: "适应宽度",
                    path: "data.isFullWidth",
                  },
                },
              ],
            },
          },
        ],
      },
    ],
  };

  static DEFAULT = {
    id: "",
    style: {},
    type: "FormImageNode",
    data: {
      isFullWidth: true,
      link: "/images/image.png",
      itemType: "style",
      imageStyle: {
        height: 100,
      },
    },
  };

  static NODE = {
    icon: "tf-icon-image",
    type: "FormImageNode",
    category: "展示组件",
    title: "图片",
    nodeData: FormImageNode.DEFAULT,
  };
}
</script>
