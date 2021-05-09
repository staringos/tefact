<template>
  <el-dialog
    title="创建组件"
    :visible="value"
    class="page-previewer"
    :before-close="handleClose"
    width="50%"
    append-to-body
    :close-on-click-modal="false"
    :close-on-press-escape="false"
  >
    <el-form>
      <el-form-item label="组件名称">
        <el-input type="text" v-model="name" @keydown.stop></el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="handleSubmit">立即创建</el-button>
        <el-button @click="handleClose">取消</el-button>
      </el-form-item>
    </el-form>
  </el-dialog>
</template>
<style lang="scss" scoped>

</style>
<script lang="ts">
import { Vue, Component, Prop } from 'vue-property-decorator'
import { BaseView } from "@tefact/core"

@Component
export default class WidgetDialog extends BaseView {
  @Prop() value!: boolean;
  @Prop(String) nodeId!: string;
  name = "";

  handleClose() {
    this.name = "";
    this.$emit("input", false);
  }

  async handleSubmit() {
    if (!this.name || this.name.length < 1)
      return this.$message.error("请输入组件名称");

    const node = this.engine.getNodeById(this.nodeId);
    const res = await this.engine.generateWidget(this.name, node);
    this.handleClose();
  }
}
</script>
