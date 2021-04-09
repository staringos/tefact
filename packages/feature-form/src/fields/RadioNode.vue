<template>
  <div class="form-node-wrapper" v-if="node">
    <el-radio
      v-model="tmpInput"
      v-for="(item, i) in node.list"
      :key="i"
      :label="item.label"
      >{{ item.label }}</el-radio
    >
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
export default class RadioNode extends Vue {
  static PROPERTIES = {
    title: "单选框配置",
    hasTab: true,
    tabs: [
      FormProperties.defaultProperties("TextRow", [
        {
          type: "ListProperties",
          params: {
            title: "选项设置",
            path: "list",
            rows: [
              {
                type: "TextRow",
                params: {
                  title: "选项标签",
                  path: "label",
                },
              },
              {
                type: "TextRow",
                params: {
                  title: "选项值",
                  path: "key",
                },
              },
            ],
          },
        },
      ]),
    ],
  };

  static DEFAULT = FormProperties.getBaseFormSection("RadioNode", {
    list: [{ label: "选项1" }, { label: "选项2" }],
  });

  static NODE = {
    icon: "tf-icon-radio",
    type: "RadioNode",
    title: "单选框",
    nodeData: RadioNode.DEFAULT,
  };
}
</script>
