<template>
  <BaseRow :title="title" v-bind="$attrs">
    <el-date-picker
      v-model="tmpText"
      :type="dateType"
      @change="handleChange"
      placeholder="请输入内容"
    ></el-date-picker>
  </BaseRow>
</template>
<script>
import { Component, Prop, Vue } from "vue-property-decorator";
import BaseRow from "./BaseRow.vue";
import RowMixin from "./RowMixin.ts";

@Component({
  components: { BaseRow },
  mixins: [RowMixin],
})
export default class DateRow extends Vue {
  @Prop([String]) dateType;
}
</script>
