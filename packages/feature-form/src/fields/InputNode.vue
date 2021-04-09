<template>
  <div class="form-node-wrapper">
    <el-input v-model="tmpInput" :placeholder="node.placeholder"></el-input>
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
export default class InputNode extends Vue {
  static PROPERTIES = {
    title: "输入框配置",
    hasTab: true,
    tabs: [FormProperties.defaultProperties("TextRow")],
  };

  static DEFAULT = FormProperties.getBaseFormSection("InputNode");

  static NODE = {
    icon: "tf-icon-input",
    type: "InputNode",
    title: "文字",
    nodeData: InputNode.DEFAULT,
  };
}
</script>
