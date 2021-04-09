<template>
  <BaseRow :title="title" v-bind="$attrs">
    <el-select
      v-if="path"
      size="small"
      :value="currentData"
      placeholder="请选择"
      @change="handleChange"
    >
      <template v-if="selectOptions">
        <el-option
          v-for="item in selectOptions"
          :key="item.value"
          :label="item.label"
          :value="item.value"
        >
        </el-option>
      </template>
    </el-select>
  </BaseRow>
</template>
<script>
import { Vue, Component, Prop } from "vue-property-decorator";
import BaseRow from "./BaseRow.vue";
import RowMixin from "./RowMixin.ts";

@Component({
  components: { BaseRow },
  mixins: [RowMixin],
})
export default class SelectResolu extends Vue {
  @Prop() selectOptions;
}
</script>
