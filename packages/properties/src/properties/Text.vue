<template>
  <BaseProperties title="文字设置" v-bind="$attrs">
    <div class="resolu-container" v-if="tmpNode">
      <div class="resolu-row">
        <div class="resolu-label">样式</div>
        <el-color-picker
          v-model="style['color']"
          @change="handleSave"
          show-alpha
        ></el-color-picker>
        <input
          type="number"
          class="resolu-input border-width"
          v-model.number="tmpNode.config.style['font-size']"
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
        <el-button-group>
          <el-button
            :type="
              style['justify-content'] === 'flex-start' ? 'primary' : 'default'
            "
            icon="tefact-icon tf-icon-youduiqi"
            size="mini"
            @click="handleStyleChange('justify-content', 'flex-start')"
          ></el-button>
          <el-button
            :type="
              style['justify-content'] === 'center' ? 'primary' : 'default'
            "
            icon="tefact-icon tf-icon-zhongduiqi"
            size="mini"
            @click="handleStyleChange('justify-content', 'center')"
          ></el-button>
          <el-button
            :type="
              style['justify-content'] === 'flex-end' ? 'primary' : 'default'
            "
            icon="tefact-icon tf-icon-zuoduiqi"
            size="mini"
            @click="handleStyleChange('justify-content', 'flex-end')"
          ></el-button>
        </el-button-group>
      </div>
      <div class="resolu-row">
        <div class="resolu-label"></div>
        <el-button-group>
          <el-button
            :type="
              style['align-items'] === 'flex-start' ? 'primary' : 'default'
            "
            icon="tefact-icon tf-icon-vertical-align-top"
            size="mini"
            @click="handleStyleChange('align-items', 'flex-start')"
          ></el-button>
          <el-button
            :type="style['align-items'] === 'center' ? 'primary' : 'default'"
            icon="tefact-icon tf-icon-vertical-align-middle"
            size="mini"
            @click="handleStyleChange('align-items', 'center')"
          ></el-button>
          <el-button
            :type="style['align-items'] === 'flex-end' ? 'primary' : 'default'"
            icon="tefact-icon tf-icon-vertical-align-bottom"
            size="mini"
            @click="handleStyleChange('align-items', 'flex-end')"
          ></el-button>
        </el-button-group>
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
import BaseProperties from "~/components/app/light/editor/properties/Base.vue";
import PropertiesMixin from "../components/PropertiesMixin";
import PropertiesClass from "../components/PropertiesClass";

@Component({
  components: { BaseProperties },
  mixins: [PropertiesMixin],
})
export default class TextProperties extends PropertiesClass {
  get isUnderline(): boolean {
    if (this.style) return this.style["text-decoration"] === "underline";
    return false;
  }

  get isBold(): boolean {
    if (this.style) return this.style["font-weight"] === "bold";
    return false;
  }

  get isItalic(): boolean {
    if (this.style) return this.style["font-style"] === "italic";
    return false;
  }
}
</script>
