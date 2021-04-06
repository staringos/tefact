<template>
  <BaseProperties title="文字设置" v-bind="$attrs">
    <div class="resolu-container" v-if="tmpNode">
      <div class="resolu-row">
        <div class="resolu-label">样式</div>
        <el-color-picker
          v-model="tmpNode.style['color']"
          @change="handleSave"
          size="small"
          show-alpha
        ></el-color-picker>
        <input
          type="number"
          style="margin-left: 10px; max-width: 80px;"
          class="properties-input"
          v-model.number="tmpNode.style['font-size']"
          @blur="handleSave"
        />px
      </div>
      <div class="resolu-row">
        <div class="resolu-label">排版</div>
        <el-button-group>
          <el-button
            :type="isBold ? 'primary' : 'default'"
            icon="tefact-icon tf-icon-jiacu"
            size="mini"
            @click="
              handleStyleChange('font-weight', isBold ? 'normal' : 'bold')
            "
          ></el-button>
          <el-button
            :type="isItalic ? 'primary' : 'default'"
            icon="tefact-icon tf-icon-qingxie"
            size="mini"
            @click="
              handleStyleChange('font-style', isItalic ? 'normal' : 'italic')
            "
          ></el-button>
          <el-button
            :type="isUnderline ? 'primary' : 'default'"
            icon="tefact-icon tf-icon-shanchuxian"
            size="mini"
            @click="
              handleStyleChange(
                'text-decoration',
                isUnderline ? 'none' : 'underline'
              )
            "
          ></el-button>
        </el-button-group>
      </div>
      <div class="resolu-row">
        <div class="resolu-label">对齐</div>
        <el-radio-group :value="tmpNode.style['justify-content']" size="mini" @input="handleChangeGenerate('justify-content')($event)">
          <el-radio-button label="flex-start">
            <i class="tefact-icon tf-icon-youduiqi"></i>
          </el-radio-button>
          <el-radio-button label="center">
            <i class="tefact-icon tf-icon-zhongduiqi"></i>
          </el-radio-button>
          <el-radio-button label="flex-end">
            <i class="tefact-icon tf-icon-zuoduiqi"></i>
          </el-radio-button>
        </el-radio-group>
      </div>
      <div class="resolu-row">
        <div class="resolu-label"></div>
        <el-radio-group :value="tmpNode.style['align-items']" size="mini" @input="handleChangeGenerate('align-items')($event)">
          <el-radio-button label="flex-start">
            <i class="tefact-icon tf-icon-vertical-align-top"></i>
          </el-radio-button>
          <el-radio-button label="center">
            <i class="tefact-icon tf-icon-vertical-align-middle"></i>
          </el-radio-button>
          <el-radio-button label="flex-end">
            <i class="tefact-icon tf-icon-vertical-align-bottom"></i>
          </el-radio-button>
        </el-radio-group>
      </div>
    </div>
  </BaseProperties>
</template>
<style lang="scss">
@import "./properties";
.field-break {
  display: block;
}
</style>
<script lang="ts">
import { Component } from "vue-property-decorator";
import BaseProperties from "./Base.vue";
import PropertiesMixin from "../components/PropertiesMixin";
import PropertiesClass from "../components/PropertiesClass";

@Component({
  components: { BaseProperties },
  mixins: [PropertiesMixin],
})
export default class TextProperties extends PropertiesClass {
  get isUnderline(): boolean {
    const style = this.tmpNode.style;
    if (style) return style["text-decoration"] === "underline";
    return false;
  }

  get isBold(): boolean {
    const style = this.tmpNode.style;
    if (style) return style["font-weight"] === "bold";
    return false;
  }

  get isItalic(): boolean {
    const style = this.tmpNode.style;
    if (style) return style["font-style"] === "italic";
    return false;
  }

  handleChangeGenerate(key: string) {
    const that = this;
    return (value: string) => {
      that.handleStyleChange(key, value);
    };
  }
}
</script>
