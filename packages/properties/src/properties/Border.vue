<template>
  <BaseProperties title="边框设置" v-bind="$attrs">
    <div class="resolu-container">
      <div class="resolu-row" v-if="tmpNode && tmpNode">
        <div class="resolu-label">边框</div>
        <el-color-picker
          v-model="tmpNode.style['border-color']"
          @change="handleSave"
          show-alpha
          size="small"
        ></el-color-picker>
        <el-select
          class="resolu-form-item border-style"
          v-model="tmpNode.style['border-style']"
          placeholder="样式"
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
          class="properties-input border-width"
          v-model.number="tmpNode.style['border-width']"
          @blur="handleSave"
        />px
      </div>
      <div class="resolu-row" v-if="tmpNode">
        <div class="resolu-label">圆角</div>
        <input
          type="number"
          class="properties-input"
          v-model.number="tmpNode.style['border-radius']"
          @blur="handleSave"
        />px
      </div>
    </div>
  </BaseProperties>
</template>

<style lang="scss" scoped>
@import "./properties";

.border-width {
  width: 30px;
  max-width: 30px;
  margin-left: 8px;
}
.border-style {
  margin-left: 5px;

  ::v-deep .el-input__inner {
    padding-left: 5px;
    padding-right: 20px;
  }

  ::v-deep .el-input__icon {
    width: 20px;
  }
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
export default class BorderProperties extends PropertiesClass {
  BorderStyle = BorderStyle;
}
</script>
