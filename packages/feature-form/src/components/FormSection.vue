<template>
  <div
    :class="`form-section
      ${!preview ? 'hover-style' : ''}
      ${active && !preview ? 'active' : ''}
      ${isMobile ? 'mobile' : ''}
    `"
    @click="handleSectionClick"
    :style="style"
    @hover.stop
    @mouseover.stop
  >
<!--    <el-form-item-->
<!--      size="small"-->
<!--      :labelWidth="`${form.config.labelWidth}px`"-->
<!--      :label="section.label"-->
<!--      :prop="section.id"-->
<!--      :required="section.notNull"-->
<!--      v-if="!isFreeFormItem"-->
<!--    >-->
<!--      <slot></slot>-->
<!--      <span class="desc">{{ section.desc }}</span>-->
<!--    </el-form-item>-->
    <el-form-item
        class="form-item-wrapper"
        size="small"
        labelWidth="10px"
        label=""
        :prop="section.id"
        :required="section.notNull"
        v-if="!isFreeFormItem"
    >
      <div class="form-item-header">
        <p class="form-item-label">{{ section.label }}</p>
        <p class="form-item-desc" v-if="section.desc">{{ section.desc }}</p>
      </div>
      <slot></slot>
    </el-form-item>
    <div class="free-form-item" v-else>
      <slot></slot>
      <span class="desc">{{ section.desc }}</span>
    </div>
    <SectionButtons
      v-if="active"
      :index="index"
      :amount="amount"
      :section="section"
    />

    <el-button
      v-if="!preview"
      class="dragging-btn handle"
      type="danger"
      size="mini"
      icon="el-icon-rank"
    ></el-button>
  </div>
</template>
<style lang="scss" scoped>
.form-section {
  width: 100%;
  box-sizing: border-box;
  padding: 10px;
  border: 1px solid transparent;
  position: relative;

  ::v-deep.el-form-item__content {
    margin-left: 10px !important;
  }

  .form-item-wrapper {
    display: flex;
    flex-direction: column;

    ::v-deep.el-form-item__content {
      flex-direction: column;
    }

    .form-item-header {
      .form-item-label {
        font-size: 14px;
      }

      .form-item-desc {
        font-size: 12px;
      }
    }
  }

  .free-form-item {
    overflow: hidden;
    height: 100%;
  }

  .dragging-btn {
    display: none;
    width: 35px;
    height: 35px;
    border: 0;
    line-height: 35px;
    padding: 0;
    position: absolute;
    top: -15px;
    left: 10px;
    font-size: 18px;
    color: #333;
  }

  &:hover {
    .dragging-btn {
      display: block;
      z-index: 999;

      &:hover {
        color: white;
      }
    }
  }

  &.mobile {
    ::v-deep.el-form-item__content {
      margin-left: 10px !important;
      display: flex;
      flex: 1;

      .el-date-editor--daterange,
      .el-date-editor--datetimerange {
        display: flex;
        flex: 1;
        width: 100%;
      }
    }
  }

  &.hover-style:hover,
  &.active {
    border: 1px solid $editor-border-active-color;
  }

  ::v-deep .el-form-item {
    display: flex;
    margin-bottom: 0;

    .el-form-item__label {
      font-size: 12px;
    }
  }

  .desc {
    margin-left: 20px;
  }
}
</style>
<script lang="ts">
import { Vue, Component, Prop } from "vue-property-decorator";
import { transformStyle } from "@tefact/utils";
import { SectionButtons } from "@tefact/ui";
import { IFormNode } from "../types";

@Component({
  components: { SectionButtons },
})
export default class FormSection extends Vue {
  @Prop() form!: IFormNode;
  @Prop() section!: IFormNode;
  @Prop(Boolean) active!: boolean;
  @Prop(Boolean) preview!: boolean;
  @Prop(Boolean) isMobile!: boolean;
  @Prop(Object) value!: any;
  @Prop(Number) index!: number;
  @Prop(Number) amount!: number;

  get style() {
    const style = transformStyle(this.section);
    if (!style["padding"] && this.section.type === 'FormImageNode') {
      style.padding = 0;
    }
    return style;
  }

  get isFreeFormItem() {
    return this.section.type === 'FormImageNode' || this.section.type === 'FormTextNode';
  }

  handleSectionClick(e: Event) {
    if (this.active) return;
    e.stopPropagation();
    this.$emit("activeChange");
  }
}
</script>
