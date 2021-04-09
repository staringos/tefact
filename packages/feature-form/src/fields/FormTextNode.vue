<template>
  <div class="form-node-wrapper" :style="style">
    {{ node.data ? node.data.text : "" }}
  </div>
</template>
<style lang="scss">
@import "./style.scss";
.form-node-wrapper {
  display: flex;
  flex: 1;
  width: 100%;
}
</style>
<script lang="ts">
import { Vue, Component } from "vue-property-decorator";
import mixin from "./mixin";
import { FormProperties } from "../config";
import { transformStyle } from "@tefact/utils";

@Component({
  mixins: [mixin],
})
export default class FormTextNode extends Vue {
  get style() {
    return transformStyle((this as any).node);
  }

  static PROPERTIES = {
    title: "描述配置",
    hasTab: true,
    tabs: [FormProperties.defaultStyledProperties()],
  };

  static DEFAULT = {
    id: "",
    style: {},
    data: {
      text: "文本描述",
      itemType: "style",
    },
    type: "FormTextNode",
  };

  static NODE = {
    icon: "tf-icon-Text",
    type: "FormTextNode",
    title: "文本描述",
    nodeData: FormTextNode.DEFAULT,
  };
}
</script>
