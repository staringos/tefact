<template>
  <BaseRow :title="title" v-bind="$attrs">
    <el-switch
      :value="current"
      active-color="#13ce66"
      inactive-color="#ff4949"
      @change="handleChange"
    >
    </el-switch>
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
export default class SelectRow extends ResoluBase {
  @Prop([String]) title
  @Prop([String]) path
  @Prop() selectOptions

  get current() {
    return get(this.tmpNode, this.path)
  }

  handleChange(e) {
    set(this.tmpNode, this.path, e)
    this.handleSave()
  }
}
</script>
