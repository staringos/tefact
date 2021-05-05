<template>
  <BaseRow :title="title" v-bind="$attrs">
    <el-select v-model="tmpText" placeholder="请选择" @change="handleChange">
      <el-option
          v-for="item in options"
          :key="item.value"
          :label="item.label"
          :value="item.value">
      </el-option>
    </el-select>
  </BaseRow>
</template>
<script>
import { Component, Prop, Vue } from "vue-property-decorator";
import BaseRow from "./BaseRow.vue";
import RowMixin from "./RowMixin.ts";
import { BaseView } from "@tefact/core";

@Component({
  components: { BaseRow },
  mixins: [RowMixin],
})
export default class TargetSelectRow extends BaseView {
  @Prop([String]) targetFeatureType;

  options = []

  async refresh() {
    if (!this.setting?.onGetTargetList) return [];
    const targets = await this.setting.onGetTargetList();
    if (!targets) return [];

    const res = [];
    targets.filter(cur => {
      if (this.targetFeatureType && cur.feature_type !== this.targetFeatureType) return;
      res.push({
        data: cur,
        label: cur.title,
        value: cur.id
      });
    })

    this.options = res;
  }

  mounted() {
    this.refresh();
  }
}
</script>
