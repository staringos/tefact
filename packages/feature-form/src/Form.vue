<template>
  <el-form
    class="form-page"
    :style="{ width: config.w, height: config.h }"
    :rules="rules"
    :model="tmpValue"
    ref="form"
  >
    <draggable
      tag="div"
      :group="{ name: 'form-item', pull: false, put: true }"
      class="list-group"
      handle=".handle"
      ghostClass="ghost"
      :animation="1"
      :sort="!preview"
      @sort="handleSort"
      @start="handleStart"
      @end="handleDragEnd"
    >
      <FormSection
        v-for="(section, index) in sections"
        :key="section.id"
        :index="index"
        :form="form"
        :amount="sections.length"
        :active="preview || !isEdit ? false : activeNodeId === section.id"
        @activeChange="handleActiveChange(section.id)"
        :section="section"
        :preview="preview"
        :isMobile="isMobile"
      >
        <component
          v-model="tmpValue[section.id]"
          :item="section"
          :is="section.type"
          :node="section"
        />
      </FormSection>
    </draggable>
    <el-form-item class="bottom-button">
      <el-button
        v-for="(button, key) in form.config.buttons"
        :type="button.styleType"
        :key="key"
        @click="handleButtonClick(button)"
        >{{ button.label }}</el-button
      >
    </el-form-item>
  </el-form>
</template>
<style lang="scss" scoped>
.form-page {
  display: flex;
  flex-direction: column;
  box-sizing: border-box;
  flex: 1;
  background-color: white;

  .bottom-button {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 60px;
  }

  .ghost {
    position: relative;
    background: #fff;
    border: 1px dashed $mainColor;

    &::after {
      display: block;
      content: "";
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background: #fff;
    }
  }
}
</style>
<script lang="ts">
import { Component, Prop, Watch } from "vue-property-decorator";
import FormSection from "./components/FormSection.vue";
import cloneDeep from "lodash/cloneDeep";
import fields from "./fields";
import draggable from "vuedraggable";
import { BaseView, EVENT } from "@tefact/core";
import { FormButton, FormRulesModel, IFormNode, IFormTarget } from "./types";
import { getSystemInfo } from "@tefact/utils";

class FormHelper {
  static initData(form: IFormTarget) {
    const res = {} as Record<string, any>;
    if (!form.config.children) form.config.children = [];
    form.config.children.forEach((item: IFormNode) => {
      res[item.id] = item.default || "";
    });
    return res;
  }

  static generateRule(form: IFormTarget) {
    const rules = {} as Record<string, any>;
    form.config?.children?.forEach((item: IFormNode) => {
      let curRules = [] as FormRulesModel[];

      if ((item as any).itemType !== "field") return;

      if (item.formRules) {
        curRules = [...item.formRules];
      }

      const thatClass = fields[item.type];

      if (thatClass.FORM_RULES) {
        curRules = [...curRules, ...thatClass.FORM_RULES];
      }

      if (item.notNull) {
        curRules.push({
          required: true,
          message: `请输入${item?.label}`,
          trigger: "blur",
        } as FormRulesModel);
      }

      rules[item.id] = curRules;
    });
    return rules;
  }
}

@Component({
  components: { FormSection, draggable, ...fields },
})
export default class Form extends BaseView {
  @Prop() form!: IFormTarget;
  @Prop() value!: any;
  @Prop(Boolean) isMobile!: boolean;
  @Prop(Boolean) preview!: boolean;
  @Prop(Boolean) isEdit!: boolean;

  tmpValue = {};
  rules = {} as any;

  get config() {
    return this.form.config || {};
  }

  get sections() {
    return this.form?.config?.children || null;
  }

  @Watch("tmpValue", { deep: true })
  handleValueChange() {}

  @Watch("form", { immediate: true })
  handleFormChange() {
    const { config } = this.form;
    this.rules = FormHelper.generateRule(this.form);

    if (this.value) {
      this.tmpValue = cloneDeep(this.value);
      return;
    }

    if (config) {
      this.tmpValue = FormHelper.initData(this.form);
    }
  }

  handleSectionIndex(index: number, oldIndex: number) {
    if (!this.sections) return;
    this.engine.resetNodeOrder(this.sections[oldIndex].id, index);
  }

  handleSort(e: any) {
    this.handleSectionIndex(e.newIndex, e.oldIndex);
  }

  handleStart() {}

  handleDragEnd() {}

  async handleSubmit() {
    const $message = (this as any).$message;
    if (!this.preview) {
      return $message({ message: "编辑状态不能提交！", type: "warning" });
    }

    const form = this.$refs.form as any;
    (form.validate as any)((valid: any) => {
      if (!valid) {
        $message.warning("请输入正确内容");
        return;
      }

      this.$emit(EVENT.FORM_DATA, {
        data: {
          data: this.tmpValue,
          submitter_info: getSystemInfo(),
        },
        id: this.form.id,
      });

      // alert("提交成功");
      // location.href = "/s/p/success";
    });
  }

  handleButtonClick(btn: FormButton) {
    switch (btn.type) {
      case "submit":
        this.handleSubmit();
        break;
      case "clear":
        this.handleClear();
        break;
    }
  }

  handleClear() {
    this.tmpValue = FormHelper.initData(this.form);
  }

  handleActiveChange(active: string) {
    this.engine.activeNode([active]);
  }
}
</script>
