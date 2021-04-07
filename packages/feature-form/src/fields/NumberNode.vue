<template>
  <div class="form-node-wrapper">
    <el-input-number
      v-model="tmpInput"
      :placeholder="node.placeholder"
    ></el-input-number>
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
export default class NumberNode extends Vue {
  static PROPERTIES = {
    title: "数字框配置",
    hasTab: true,
    tabs: [FormProperties.defaultProperties("NumberRow")],
  };
  static DEFAULT = FormProperties.getBaseFormSection("NumberNode");

  static NODE = {
    icon: "tf-icon-number",
    type: "NumberNode",
    category: "表单组件",
    title: "数字",
    nodeData: NumberNode.DEFAULT,
  };
}
</script>
