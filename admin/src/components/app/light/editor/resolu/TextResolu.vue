<template>
  <BaseResolu title="文字设置" v-bind="$attrs">
    <div class="resolu-container" v-if="tmpNode">
      <div class="resolu-row">
        <div class="resolu-label">样式</div>
        <el-color-picker v-model="style['color']" @change="handleSave" show-alpha></el-color-picker>
        <input type="number" class="resolu-input border-width" v-model.number="tmpNode.config.style['font-size']" @blur="handleSave" />px
      </div>
      <div class="resolu-row">
        <div class="resolu-label">排版</div>
        <el-button-group>
          <el-button
            :type="isBold ? 'primary' : 'default'"
            icon="tefact-icon tf-icon-jiacu"
            size="mini"
            @click="handleStyleChange('font-weight', isBold ? 'none' : 'bold')"
          ></el-button>
          <el-button
            :type="isItalic ? 'primary' : 'default'"
            icon="tefact-icon tf-icon-qingxie"
            size="mini"
            @click="handleStyleChange('font-style', isItalic ? 'none' : 'italic')"
          ></el-button>
          <el-button
            :type="isUnderline ? 'primary' : 'default'"
            icon="tefact-icon tf-icon-shanchuxian"
            size="mini"
            @click="handleStyleChange('text-decoration', isUnderline ? 'none' : 'underline')"
          ></el-button>
        </el-button-group>
      </div>
      <div class="resolu-row">
        <div class="resolu-label">对齐</div>
        <el-button-group>
          <el-button :type="style['justify-content'] === 'flex-start' ? 'primary' : 'default'" icon="tefact-icon tf-icon-youduiqi" size="mini" @click="handleStyleChange('justify-content', 'flex-start')"></el-button>
          <el-button :type="style['justify-content'] === 'center' ? 'primary' : 'default'" icon="tefact-icon tf-icon-zhongduiqi" size="mini" @click="handleStyleChange('justify-content', 'center')"></el-button>
          <el-button :type="style['justify-content'] === 'flex-end' ? 'primary' : 'default'" icon="tefact-icon tf-icon-zuoduiqi" size="mini" @click="handleStyleChange('justify-content', 'flex-end')"></el-button>
        </el-button-group>
      </div>
      <div class="resolu-row">
        <div class="resolu-label"></div>
        <el-button-group>
          <el-button :type="style['align-items'] === 'flex-start' ? 'primary' : 'default'" icon="tefact-icon tf-icon-vertical-align-top" size="mini" @click="handleStyleChange('align-items', 'flex-start')"></el-button>
          <el-button :type="style['align-items'] === 'center' ? 'primary' : 'default'" icon="tefact-icon tf-icon-vertical-align-middle" size="mini" @click="handleStyleChange('align-items', 'center')"></el-button>
          <el-button :type="style['align-items'] === 'flex-end' ? 'primary' : 'default'" icon="tefact-icon tf-icon-vertical-align-bottom" size="mini" @click="handleStyleChange('align-items', 'flex-end')"></el-button>
        </el-button-group>
      </div>
    </div>
  </BaseResolu>
</template>
<style lang="scss">
  @import "./resolu";
  .field-break {
    display: block;
  }
</style>
<script lang="ts">
  import { Vue, Component, Prop } from 'nuxt-property-decorator'
  import BaseResolu from '~/components/app/light/editor/resolu/BaseResolu.vue'
  import ResoluMixin from '~/components/app/light/editor/resolu/ResoluMixin'
  import ResoluBase from "~/components/app/light/editor/resolu/ResoluClass";

  @Component({
    components: { BaseResolu },
    mixins: [ ResoluMixin ]
  })
  export default class TextResolu extends ResoluBase {

    get isUnderline() {
      if (this.style)
        return this.style['text-decoration'] === 'underline'
    }

    get isBold() {
      if (this.style)
        return this.style['font-weight'] === 'bold'
    }
    get isItalic() {
      if (this.style)
        return this.style['font-style'] === 'italic'
    }
  }
</script>
