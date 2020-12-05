<template>
  <BaseRow :title="title" v-bind="$attrs">
    <el-input-number v-model="tmpText" size="mini" @blur="handleChange" placeholder=""></el-input-number>
    <span>{{unit}}</span>
  </BaseRow>
</template>
<script>
import get from 'lodash/get'
import set from 'lodash/set'
import { Component, Prop, Watch } from 'nuxt-property-decorator'
import ResoluMixin from '~/components/app/light/editor/resolu/ResoluMixin'
import ResoluBase from '~/components/app/light/editor/resolu/ResoluClass'
import BaseRow from '~/components/app/light/editor/resolu/rows/BaseRow.vue'
import RowMixin from '~/components/app/light/editor/resolu/rows/RowMixin.ts'

@Component({
  components: { BaseRow },
  mixins: [ ResoluMixin, RowMixin ]
})
export default class TextRow extends ResoluBase {
  @Prop([String]) title
  @Prop([String]) path
  @Prop([String]) unit
  @Prop() selectOptions

  tmpText = ''

  @Watch('tmpNode', { deep: true, immediate: true })
  handleTmpNodeChange() {
    this.tmpText = get(this.tmpNode, this.path)
  }

  handleChange() {
    set(this.tmpNode, this.path, this.tmpText)
    this.handleSave()
  }
}
</script>
