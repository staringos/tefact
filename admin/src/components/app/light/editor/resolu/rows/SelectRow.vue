<template>
  <BaseRow :title="title" v-bind="$attrs">
    <el-select v-if="path" size="small" :value="selectData" placeholder="请选择" @change="handleChange">
      <template v-if="selectOptions">
        <el-option
          v-for="item in selectOptions"
          :key="item.value"
          :label="item.label"
          :value="item.value">
        </el-option>
      </template>
    </el-select>
  </BaseRow>
</template>
<script>
import get from 'lodash/get'
import set from 'lodash/set'
import { Component, Prop } from "nuxt-property-decorator";
import ResoluMixin from '~/components/app/light/editor/resolu/ResoluMixin'
import ResoluBase from '~/components/app/light/editor/resolu/ResoluClass'
import BaseRow from '~/components/app/light/editor/resolu/rows/BaseRow.vue'
import RowMixin from "@/components/app/light/editor/resolu/rows/RowMixin.ts";

@Component({
  components: { BaseRow },
  mixins: [ ResoluMixin, RowMixin ]
})
export default class SelectResolu extends ResoluBase {
  @Prop([String]) title
  @Prop([String]) path
  @Prop() selectOptions

  get selectData() {
    return get(this.tmpNode, this.path)
  }

  handleChange(e) {
    set(this.tmpNode, this.path, e)
    this.handleSave()
  }
}
</script>
