<template>
  <BaseProperties :title="title" v-bind="$attrs">
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
  </BaseProperties>
</template>
<script>
import { Component, Prop } from "vue-property-decorator";
import BaseProperties from "./Base.vue";
import PropertiesMixin from "../components/PropertiesMixin";
import PropertiesClass from "../components/PropertiesClass";
import Rows from "../rows";

@Component({
  components: { BaseProperties, ...Rows },
  mixins: [PropertiesMixin],
})
export default class SelectProperties extends PropertiesClass {
  @Prop([Array]) rows;
  @Prop([String]) title;
}
</script>
