<template>
  <BaseNode
    v-bind="$attrs"
    v-on="$listeners"
    :node="node"
    :sectionId="sectionId"
    :preview="preview"
    class="form-node"
  >
    <Form
      v-if="form"
      :form="form"
      :preview="preview"
      @submit="setting.onFormDataSubmit"
    />
    <div v-if="!form && !preview" class="form-unselect">
      <el-button
        type="primary"
        size="mini"
        icon="el-icon-plus"
        @click="handleChoose"
        >选择表单</el-button
      >
      <el-button size="mini" icon="el-icon-thumb" @click="handleAdd"
        >新增表单</el-button
      >
    </div>
  </BaseNode>
</template>
<style lang="scss" scoped>
.form-node {
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: $gray-01;
  position: relative;

  .main {
    width: 100%;
    height: 100%;
  }

  .form-unselect {
    width: 100%;
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
  }
}
</style>
<script lang="ts">
import { Component, Watch } from "vue-property-decorator";
import BaseNode from "./BaseNode.vue";
import NodeClass from "./NodeClass";
import Form from "@tefact/feature-form";
import { FreeNodeData, getBaseNode, IBaseNode, ITarget } from "@tefact/core";
import { PageProperties } from "../config";
import { EVENT_INSIDE } from "@tefact/core";

@Component({
  components: { Form, BaseNode },
})
export default class FormNode extends NodeClass<IBaseNode> {
  editor: any = null;
  form: ITarget | null = null;

  get selected() {
    return !!this.nodeData.formId;
  }

  handleChoose() {
    this.engine.emit(EVENT_INSIDE.SWITCH_PROPERTIES_TAB, "1");
  }
  handleAdd() {
    this.engine.targetAdd();
  }

  @Watch("node.data.formId", { immediate: true })
  async handleFormIdChange() {
    this.getData();
  }

  async getData() {
    if (!this.nodeData.formId) return null;
    this.form = await this.engine.getTargetById(this.nodeData.formId);
  }

  static DEFAULT = {
    ...getBaseNode(350, 390),
    type: "FormNode",
    data: {
      formId: null,
    } as FreeNodeData,
  } as IBaseNode;

  static NODE = {
    icon: "tf-icon-form",
    type: "FormNode",
    title: "表单",
    nodeData: FormNode.DEFAULT,
  };

  static PROPERTIES = PageProperties.defaultProperties("网页配置", [
    {
      type: "FormProperties",
      params: {
        title: "内容设置",
      },
    },
  ]);
}
</script>
