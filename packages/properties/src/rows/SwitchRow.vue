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
import { Component, Vue } from "vue-property-decorator";
import BaseRow from "./BaseRow.vue";
import RowMixin from "./RowMixin.ts";

@Component({
  components: { BaseRow },
  mixins: [RowMixin],
})
export default class SwitchRow extends Vue {}
</script>
