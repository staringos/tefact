<template>
  <BaseResolu :title="title" v-bind="$attrs">
    <template v-if="node && nodeType">
      <component
        v-for="(row, i) in rows"
        :key="i"
        :index="i"
        :is="row.type"
        :nodeType="nodeType"
        :node="node"
        v-bind="row.params"
        :row="row"
      ></component>
    </template>
  </BaseResolu>
</template>
<script>
import { Component, Prop } from "nuxt-property-decorator";
import BaseResolu from '~/components/app/light/editor/resolu/BaseResolu.vue'
import ResoluMixin from '~/components/app/light/editor/resolu/ResoluMixin'
import ResoluBase from '~/components/app/light/editor/resolu/ResoluClass'
import SelectRow from '~/components/app/light/editor/resolu/rows/SelectRow'
import SwitchRow from '~/components/app/light/editor/resolu/rows/SwitchRow'
import TextRow from '~/components/app/light/editor/resolu/rows/TextRow'
import TextareaRow from '~/components/app/light/editor/resolu/rows/TextareaRow'

@Component({
  components: { BaseResolu, SelectRow, SwitchRow, TextRow, TextareaRow },
  mixins: [ ResoluMixin ]
})
export default class SelectResolu extends ResoluBase {
  @Prop([Array]) rows
  @Prop([String]) title
}
</script>
