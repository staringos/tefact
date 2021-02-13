<template>
  <div class="form-node-wrapper">
    <el-input
      prefix-icon="tefact-icon tf-icon-phone"
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
import { verifyPhone } from "@tefact/utils";

@Component({
  mixins: [mixin],
})
export default class PhoneNode extends Vue {
  static PROPERTIES = {
    title: "手机号配置",
    hasTab: true,
    tabs: [FormProperties.defaultProperties("TextRow")],
  };

  static FORM_RULES = [
    {
      validator(rule: any, value: string, callback: any) {
        if (value === "" || !value) {
          return callback();
        }

        if (!verifyPhone(value)) {
          return callback(new Error("请再次输入密码"));
        }

        callback();
      },
      message: `请输入正确的电话号码`,
      trigger: "blur",
    },
  ];

  static DEFAULT = FormProperties.getBaseFormSection("PhoneNode");

  static NODE = {
    icon: "tf-icon-phone",
    type: "PhoneNode",
    title: "手机号",
    nodeData: PhoneNode.DEFAULT,
  };
}
</script>
