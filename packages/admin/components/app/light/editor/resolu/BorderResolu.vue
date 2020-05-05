<template>
  <BaseResolu title="边框设置" v-bind="$attrs">
    <div class="resolu-container">
      <div class="resolu-row" v-if="tmpNode">
        <div class="resolu-label">边框</div>
        <el-color-picker v-model="tmpNode.config.style['border-color']" @change="handleSave" show-alpha  size="small"></el-color-picker>
        <el-select class="resolu-form-item" v-model="tmpNode.config.style['border-style']" placeholder="边框样式" size="small" @change="handleSave">
          <el-option
            v-for="item in BorderStyle"
            :key="item.value"
            :label="item.label"
            :value="item.value">
          </el-option>
        </el-select>
        <input type="number" class="resolu-input border-width" v-model.number="tmpNode.config.style['border-width']" @blur="handleSave" />px
      </div>
    </div>
  </BaseResolu>
</template>
<style lang="scss">
  @import "./resolu";

  .border-width {
    width: 50px;
    margin-left: 10px;
  }
</style>
<script lang="ts">
  import { Vue, Component } from "nuxt-property-decorator";
  import BaseResolu from '~/components/app/light/editor/resolu/BaseResolu.vue'
  import { BorderStyle } from "~/utils/constants/Editor";
  import ResoluMixin from '~/components/app/light/editor/resolu/ResoluMixin'
  import ResoluBase from "~/components/app/light/editor/resolu/ResoluClass";

  @Component({
    components: { BaseResolu },
    mixins: [ ResoluMixin ]
  })
  export default class BorderResolu extends ResoluBase {
    BorderStyle=BorderStyle
  }
</script>
