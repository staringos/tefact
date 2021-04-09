<template>
  <BaseProperties title="位置大小" v-bind="$attrs">
    <div class="resolu-container" v-if="tmpNode">
      <div class="resolu-row" v-if="!onlySize">
        <div class="resolu-label">位置</div>
        <div class="content">
          <input
            type="number"
            class="properties-input half"
            v-model.number="tmpNode.pos.x"
            @blur="handleSave"
          />
          <input
            type="number"
            class="properties-input half"
            v-model.number="tmpNode.pos.y"
            @blur="handleSave"
          />
        </div>
      </div>
      <div class="resolu-row">
        <div class="resolu-label">大小</div>
        <input
          type="number"
          class="properties-input half"
          v-model.number="tmpNode.pos.w"
          @blur="handleSave"
        />
        <input
          type="number"
          class="properties-input half"
          v-model.number="tmpNode.pos.h"
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
export default class PositionProperties extends PropertiesClass {
  @Prop() sectionId!: string;
  @Prop() onlySize!: boolean;
}
</script>
