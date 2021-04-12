<template>
  <BaseProperties title="位置大小" v-bind="$attrs">
    <div class="resolu-container" v-if="tmpNode">
      <div class="resolu-row" v-if="!onlySize">
        <div class="resolu-label">位置</div>
        <div class="content">
          <PropertyNumberInput
            type="number"
            class="properties-input half"
            v-model.number="tmpNode.pos.x"
            :min="1"
            @save="handleSave"
          />
          <PropertyNumberInput
            type="number"
            class="properties-input half"
            v-model.number="tmpNode.pos.y"
            :min="1"
            @save="handleSave"
          />
        </div>
      </div>
      <div class="resolu-row">
        <div class="resolu-label">大小</div>
        <PropertyNumberInput
          type="number"
          class="properties-input half"
          v-model.number="tmpNode.pos.w"
          :min="1"
          @save="handleSave"
        />
        <PropertyNumberInput
          type="number"
          class="properties-input half"
          v-model.number="tmpNode.pos.h"
          :min="1"
          @save="handleSave"
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
import { PropertyNumberInput } from "@tefact/ui";

@Component({
  components: { BaseProperties, PropertyNumberInput },
  mixins: [PropertiesMixin],
})
export default class PositionProperties extends PropertiesClass {
  @Prop() sectionId!: string;
  @Prop() onlySize!: boolean;
}
</script>
