<template>
  <input
    type="number"
    class="properties-input half"
    v-model="tmpValue"
    :min="min"
    :max="max"
    v-bind="$listeners"
    @input="handleInput"
    @blur="handleSave"
    @keydown.enter="handleSave"
  />
</template>
<script lang="ts">
import { Component, Prop, Vue, Watch } from "vue-property-decorator";
import isNumber from "lodash/isnumber";
import toNumber from "lodash/toNumber";

@Component
export default class PropertyInput extends Vue {
  tmpValue = undefined;

  @Prop(Number) value!: number;
  @Prop(Number) max!: number;
  @Prop(Number) min!: number;

  @Watch("value", { immediate: true })
  handleValueChange() {
    this.tmpValue = this.value as any;
  }

  inputMaxMin() {
    const value = toNumber(this.tmpValue);

    if (isNumber(this.min) && value < this.min) {
      Vue.set(this, "tmpValue", this.min);
      this.handleInput();
    }

    if (isNumber(this.max) && value > this.max) {
      Vue.set(this, "tmpValue", this.max);
      this.handleInput();
    }
  }

  handleSave() {
    this.inputMaxMin();
    this.$emit("save");
  }

  handleInput() {
    this.$emit("input", this.tmpValue)
  }
}
</script>
<style lang="scss">
.properties-input {
  background: $gray-02;
  border: 0;
  height: 30px;
  padding-left: 10px;
  flex: 1;
  margin-right: 10px;

  &:focus {
    outline-offset: 0;
    outline: none;
    border: 0;
  }

  &.half {
    width: 50%;
  }
}

</style>
