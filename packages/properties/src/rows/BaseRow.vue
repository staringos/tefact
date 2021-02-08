<template>
  <div class="resolu-row">
    <div class="resolu-rows-label">{{ title }}</div>
    <div class="resolu-rows-content">
      <slot></slot>
    </div>
  </div>
</template>
<script>
import { Component, Prop } from "vue-property-decorator";
import PropertiesMixin from "../components/PropertiesMixin";
import PropertiesClass from "../components/PropertiesClass";

@Component({
  mixins: [PropertiesMixin],
})
export default class BaseRows extends PropertiesClass {
  @Prop([String]) title;
  @Prop([String]) row;
}
</script>
<style lang="scss" scoped>
.resolu-row {
  margin-bottom: 10px;
  display: flex;
  align-items: center;

  .resolu-rows-label {
    display: block;
    line-height: 40px;
    margin-right: 10px;
    width: 60px;
  }

  .resolu-rows-content {
    flex: 1;
  }
}
</style>
