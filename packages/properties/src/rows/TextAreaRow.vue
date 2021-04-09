<template>
  <BaseRow :title="title" v-bind="$attrs">
    <el-input
      v-model="tmpText"
      type="textarea"
      @change="handleChange"
      placeholder="请输入内容"
    ></el-input>
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
export default class TextAreaRow extends Vue {}
</script>
