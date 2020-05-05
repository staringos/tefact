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

        <el-button-group class="resolu-form-item">
          <el-button :type="style['text-align'] === 'left' ? 'primary' : 'default'" icon="tefact-icon tf-icon-youduiqi" size="mini" @click="handleStyleChange('text-align', 'left')"></el-button>
          <el-button :type="style['text-align'] === 'center' ? 'primary' : 'default'" icon="tefact-icon tf-icon-zhongduiqi" size="mini" @click="handleStyleChange('text-align', 'center')"></el-button>
          <el-button :type="style['text-align'] === 'right' ? 'primary' : 'default'" icon="tefact-icon tf-icon-zuoduiqi" size="mini" @click="handleStyleChange('text-align', 'right')"></el-button>
        </el-button-group>
      </div>
    </div>
  </BaseResolu>
</template>
<style lang="scss">
  @import "./resolu";
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
