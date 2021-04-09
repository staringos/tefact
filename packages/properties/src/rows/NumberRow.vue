<template>
  <BaseRow :title="title" v-bind="$attrs">
    <el-input-number
      v-model="tmpText"
      size="mini"
      @blur="() => handleChange(tmpText)"
      placeholder=""
    ></el-input-number>
    <span class="text"> {{ unit }}</span>
  </BaseRow>
</template>
<script>
import { Component, Prop } from "vue-property-decorator";
import BaseRow from "./BaseRow.vue";
import RowMixin from "./RowMixin.ts";
import { BaseView } from "@tefact/core/src";

@Component({
  components: { BaseRow },
  mixins: [RowMixin],
})
export default class NumberRow extends BaseView {
  @Prop(String) unit;
}
</script>
<style lang="scss" scoped>
.text {
  margin-left: 5px;
}
</style>
