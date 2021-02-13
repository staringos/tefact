<template>
  <div class="form-node-wrapper">
    <img :src="node.link" :style="style" />
  </div>
</template>
<style lang="scss">
@import "./style.scss";
.form-node-wrapper {
  position: relative;
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
    const { isFullWidth, imageStyle } = (this as any).config;
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
                    path: "link",
                  },
                },
                {
                  type: "NumberRow",
                  params: {
                    title: "宽度",
                    path: "imageStyle.width",
                  },
                },
                {
                  type: "NumberRow",
                  params: {
                    title: "高度",
                    path: "imageStyle.height",
                  },
                },
                {
                  type: "SwitchRow",
                  params: {
                    title: "适应宽度",
                    path: "isFullWidth",
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
    imageStyle: {
      height: 100,
    },
    isFullWidth: true,
    link: "/images/image.png",
    itemType: "style",
    type: "FormImageNode",
  };

  static NODE = {
    icon: "tf-icon-image",
    type: "FormImageNode",
    title: "图片",
    nodeData: FormImageNode.DEFAULT,
  };
}
</script>
