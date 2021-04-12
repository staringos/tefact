<template>
  <div class="form-node-wrapper">
    <el-rate v-model="tmpInput"></el-rate>
  </div>
</template>
<style lang="scss" scoped>
@import "./style.scss";

.form-node-wrapper {
  display: flex;
  height: 100%;
  align-items: center;
}
</style>
<script lang="ts">
import { Vue, Component } from "vue-property-decorator";
import mixin from "./mixin";
import { FormProperties } from "../config";

@Component({
  mixins: [mixin],
})
export default class StarNode extends Vue {
  static PROPERTIES = {
    title: "评分配置",
    hasTab: true,
    tabs: [FormProperties.defaultProperties("TextRow")],
  };

  static DEFAULT = FormProperties.getBaseFormSection("StarNode");

  static NODE = {
    icon: "tf-icon-star",
    type: "StarNode",
    category: "表单组件",
    title: "评分",
    nodeData: StarNode.DEFAULT,
  };
}
</script>
