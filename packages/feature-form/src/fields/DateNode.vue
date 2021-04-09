<template>
  <div class="form-node-wrapper">
    <el-date-picker
      v-model="tmpInput"
      :type="node.dateType"
      :placeholder="node.placeholder"
    >
    </el-date-picker>
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
export default class DateNode extends Vue {
  static PROPERTIES = {
    title: "日期框配置",
    hasTab: true,
    tabs: [
      FormProperties.defaultProperties("DateRow", null, [
        {
          type: "SelectRow",
          params: {
            title: "类型",
            path: "dateType",
            selectOptions: [
              { value: "date", label: "日期" },
              { value: "datetime", label: "日期时间" },
              { value: "daterange", label: "日期范围" },
              { value: "datetimerange", label: "日期时间范围" },
            ],
          },
        },
      ]),
    ],
  };

  static DEFAULT = FormProperties.getBaseFormSection("DateNode", {
    dateType: "date",
  });

  static NODE = {
    icon: "tf-icon-date",
    type: "DateNode",
    title: "日期",
    nodeData: DateNode.DEFAULT,
  };
}
</script>
