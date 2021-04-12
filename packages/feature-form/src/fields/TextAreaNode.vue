<template>
  <div class="form-node-wrapper">
    <el-input
      type="textarea"
      v-model="tmpInput"
      :placeholder="node.placeholder"
    ></el-input>
  </div>
</template>
<style lang="scss">
@import "./style.scss";
</style>
<script lang="ts">
import { Vue, Component } from "vue-property-decorator";
import mixin from "./mixin";
import { FormProperties } from "../config";

@Component({
  mixins: [mixin],
})
export default class TextAreaNode extends Vue {
  static PROPERTIES = {
    title: "多行文本配置",
    hasTab: true,
    tabs: [FormProperties.defaultProperties("TextAreaRow")],
  };

  static DEFAULT = FormProperties.getBaseFormSection("TextAreaNode");

  static NODE = {
    icon: "tf-icon-textarea",
    type: "TextAreaNode",
    category: "表单组件",
    title: "多行文本",
    nodeData: TextAreaNode.DEFAULT,
  };
}
</script>
