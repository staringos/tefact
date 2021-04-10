<template>
  <BaseRow :title="title" v-bind="$attrs">
    <p class="notice-row">
      <i class="notice-row-icon" :class="icon || 'el-icon-warning-outline'"></i>
      {{label}}
    </p>
  </BaseRow>
</template>
<script>
import { Component, Prop } from "vue-property-decorator";
import BaseRow from "./BaseRow.vue";
import RowMixin from "./RowMixin.ts";
import { BaseView } from "@tefact/core/src";
import { PropertyNumberInput } from "@tefact/ui";

@Component({
  components: { BaseRow, PropertyNumberInput },
  mixins: [RowMixin],
})
export default class NoticeRow extends BaseView {
  @Prop(String) label;
  @Prop(String) icon;
}
</script>
<style lang="scss" scoped>
.text {
  margin-left: 5px;
}
</style>
<style lang="scss" scoped>
.notice-row {
  font-size: 12px;
  color: #bababa;
}
.notice-row-icon {
  font-size: 12px;
}
</style>
