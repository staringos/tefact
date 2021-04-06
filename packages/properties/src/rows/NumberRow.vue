<template>
  <BaseRow :title="title" v-bind="$attrs">
    <!--    <el-input-number-->
    <!--      v-model="tmpText"-->
    <!--      size="mini"-->
    <!--      @blur="() => handleChange(tmpText)"-->
    <!--      placeholder=""-->
    <!--    ></el-input-number>-->

    <PropertyNumberInput
      type="number"
      v-model.number="tmpText"
      :min="1"
      @save="handleChange(tmpText)"
    />
    <span class="text"> {{ suffix }}</span>
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
export default class NumberRow extends BaseView {
  @Prop(String) suffix;
}
</script>
<style lang="scss" scoped>
.text {
  margin-left: 5px;
}
</style>
