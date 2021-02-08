<template>
  <BaseProperties title="边框设置" v-bind="$attrs">
    <div class="resolu-container">
      <div class="resolu-row" v-if="tmpNode && tmpNode.config">
        <div class="resolu-label">边框</div>
        <el-color-picker
          v-model="tmpNode.config.style['border-color']"
          @change="handleSave"
          show-alpha
          size="small"
        ></el-color-picker>
        <el-select
          class="resolu-form-item"
          v-model="tmpNode.config.style['border-style']"
          placeholder="边框样式"
          size="small"
          @change="handleSave"
        >
          <el-option
            v-for="item in BorderStyle"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          >
          </el-option>
        </el-select>
        <input
          type="number"
          class="resolu-input border-width"
          v-model.number="tmpNode.config.style['border-width']"
          @blur="handleSave"
        />px
      </div>
      <div class="resolu-row" v-if="tmpNode && tmpNode.config">
        <div class="resolu-label">圆角</div>
        <input
          type="number"
          class="resolu-input border-width"
          v-model.number="tmpNode.config.style['border-radius']"
          @blur="handleSave"
        />px
      </div>
    </div>
  </BaseProperties>
</template>
<style lang="scss">
@import "./properties";

.border-width {
  width: 50px;
  margin-left: 10px;
}
</style>
<script lang="ts">
import { Component } from "vue-property-decorator";
import BaseProperties from "./Base.vue";
import PropertiesMixin from "../components/PropertiesMixin";
import PropertiesClass from "../components/PropertiesClass";

export const BorderStyle = [
  { value: "solid", label: "直线" },
  { value: "dotted", label: "短虚线" },
  { value: "dashed", label: "长虚线" },
  { value: "double", label: "双层" },
];

@Component({
  components: { BaseProperties },
  mixins: [PropertiesMixin],
})
export default class BorderResolu extends PropertiesClass {
  BorderStyle = BorderStyle;
}
</script>
