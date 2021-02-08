<template>
  <BaseRow :title="title" v-bind="$attrs">
    <el-switch
      :value="currentData"
      active-color="#13ce66"
      inactive-color="#ff4949"
      @change="handleChange"
    >
    </el-switch>
  </BaseRow>
</template>
<script>
import { Component } from "vue-property-decorator";
import BaseRow from "~/components/app/light/editor/properties/rows/BaseRow.vue";
import RowMixin from "./RowMixin.ts";

@Component({
  components: { BaseRow },
  mixins: [RowMixin],
})
export default class SwitchRow {}
</script>
