<template>
  <div class="form-node-wrapper" v-if="node">
    <el-select v-model="tmpInput" :multiple="node.multiple" :filterable="true">
      <el-option
        v-for="(item, i) in node.list"
        :key="i"
        :label="item.label"
        :value="item.key"
      />
    </el-select>
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
export default class SelectNode extends Vue {
  static PROPERTIES = {
    title: "下拉框配置",
    hasTab: true,
    tabs: [
      FormProperties.defaultProperties(
        "TextRow",
        [
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
        ],
        [
          {
            type: "SwitchRow",
            params: {
              title: "是否多选",
              path: "multiple",
            },
          },
        ]
      ),
    ],
  };

  static DEFAULT = FormProperties.getBaseFormSection("SelectNode", {
    list: [
      { label: "选项1", key: 1 },
      { label: "选项2", key: 2 },
    ],
  });

  static NODE = {
    icon: "tf-icon-select",
    type: "SelectNode",
    title: "下拉框",
    nodeData: SelectNode.DEFAULT,
  };
}
</script>
