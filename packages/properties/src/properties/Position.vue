<template>
  <BaseProperties title="位置大小" v-bind="$attrs">
    <div class="resolu-container" v-if="tmpNode">
      <div class="resolu-row" v-if="!onlySize">
        <div class="resolu-label">位置</div>
        <input
          type="number"
          class="resolu-input"
          v-model.number="tmpNode.config.x"
          @blur="handleSave"
        />
        <input
          type="number"
          class="resolu-input"
          v-model.number="tmpNode.config.y"
          @blur="handleSave"
        />
      </div>
      <div class="resolu-row">
        <div class="resolu-label">大小</div>
        <input
          type="number"
          class="resolu-input"
          v-model.number="tmpNode.config.w"
          @blur="handleSave"
        />
        <input
          type="number"
          class="resolu-input"
          v-model.number="tmpNode.config.h"
          @blur="handleSave"
        />
      </div>
    </div>
  </BaseProperties>
</template>
<style lang="scss" scoped>
@import "./properties";
</style>
<script lang="ts">
import { Component, Prop } from "vue-property-decorator";
import BaseProperties from "./Base.vue";
import PropertiesMixin from "../components/PropertiesMixin";
import PropertiesClass from "../components/PropertiesClass";

@Component({
  components: { BaseProperties },
  mixins: [PropertiesMixin],
})
export default class PositionResolu extends PropertiesClass {
  @Prop() sectionId!: string;
  @Prop() onlySize!: boolean;

  mounted() {}
}
</script>
