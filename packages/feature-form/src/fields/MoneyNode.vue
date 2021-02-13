<template>
  <div class="form-node-wrapper">
    <el-input
      type="number"
      v-model="tmpInput"
      prefix-icon="tefact-icon tf-icon-money"
      :precision="2"
      :placeholder="node.placeholder"
      step="0.01"
      @blur="handleBlur"
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
export default class MoneyNode extends Vue {
  handleBlur() {
    const that = this as any;
    that.tmpInput = Math.floor(that.tmpInput * 100) / 100;
  }

  static PROPERTIES = {
    title: "价格配置",
    hasTab: true,
    tabs: [FormProperties.defaultProperties("NumberRow")],
  };

  static DEFAULT = FormProperties.getBaseFormSection("MoneyNode");

  static NODE = {
    icon: "tf-icon-money",
    type: "MoneyNode",
    title: "价格",
    nodeData: MoneyNode.DEFAULT,
  };
}
</script>
