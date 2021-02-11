<template>
  <BaseNode
    v-bind="$attrs"
    v-on="$listeners"
    :node="node"
    :sectionId="sectionId"
    :preview="preview"
    class="form-node"
  >
    <Form v-if="selected" :form="form" :preview="preview" />
    <div v-if="!selected && !preview" class="form-unselect">
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
import Form, { DefaultForm } from "@tefact/feature-form";
import cloneDeep from "lodash/cloneDeep";
// import {
//   EVENT_EDITOR_SWITCH_TAB,
//   getBaseNodeConfig,
//   PageProperties,
// } from "~/utils/constants/Editor";
import { FreeNodeData, getBaseNode, IBaseNode } from "@tefact/core";
import { PageProperties } from "../config";
import { EVENT_INSIDE } from "@tefact/core";

@Component({
  components: { Form, BaseNode },
})
export default class FormNode extends NodeClass<IBaseNode> {
  editor: any = null;
  form = cloneDeep(DefaultForm);

  // @system.Getter uploadUrl;
  // @editor.Action modifyNode;
  // @editor.Action getFormById;

  get selected() {
    return !!this.nodeData.formId;
  }

  handleChoose() {
    this.engine.emit(EVENT_INSIDE.SWITCH_PROPERTIES_TAB, "1");
  }
  handleAdd() {}

  @Watch("node.data.formId", { immediate: true })
  async handleFormIdChange() {
    // TODO good way to get form list
    // this.form = await this.getFormById({ id: (this.node as any).data.formId });
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
