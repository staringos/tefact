<template>
  <BaseRow :title="title" v-bind="$attrs">
    <el-input
      v-if="type !== 'number'"
      :type="type"
      v-model="tmpText"
      size="small"
      @blur="handleChange(tmpText)"
      placeholder="请输入内容"
    ></el-input>
    <el-input-number
      v-if="type === 'number'"
      size="small"
      :type="type"
      v-model="tmpText"
      @blur="handleChange(tmpText)"
      placeholder="请输入内容"
    ></el-input-number>
    <span>{{ suffix }}</span>
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
export default class TextRow extends Vue {
  @Prop(String) suffix;
  @Prop({ type: String, default: "text" }) type;
}
</script>
