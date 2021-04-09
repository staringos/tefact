<template>
  <div class="form-node-wrapper" v-if="node">
    <el-checkbox-group v-model="tmpInput">
      <el-checkbox
        v-for="(item, i) in node.list"
        :key="item.key || i"
        :label="item.label"
        >{{ item.label }}</el-checkbox
      >
    </el-checkbox-group>
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
export default class CheckboxNode extends Vue {
  originDate = [];

  static PROPERTIES = {
    title: "复选框配置",
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

  static DEFAULT = FormProperties.getBaseFormSection("CheckboxNode", {
    list: [
      { label: "选项1", key: "1" },
      { label: "选项2", key: "2" },
    ],
  });

  static NODE = {
    icon: "tf-icon-checkbox",
    type: "CheckboxNode",
    title: "复选框",
    nodeData: CheckboxNode.DEFAULT,
  };
}
</script>
