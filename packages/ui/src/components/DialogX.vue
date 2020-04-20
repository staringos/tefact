<template>
  <el-dialog
    :title="title"
    :visible="visible"
    :width="width"
    :close-on-press-escape="closeOnPressEscape"
    :before-close="handleClose"
    :show-close="showClose">
    <slot></slot>
    <slot name="footer" slot="footer"></slot>
  </el-dialog>
</template>
<script lang="ts">
  import { Vue, Component, namespace, Prop, Emit } from 'nuxt-property-decorator'

  const system = namespace('system')

  @Component
  export default class DialogX extends Vue {
    @Prop(String) DialogKey
    @Prop(String) title
    @Prop({ default: '30%' }) width
    @Prop({ default: false }) closeOnPressEscape
    @Prop({ default: true }) showClose

    @system.Getter DIALOG_NAME
    @system.Getter dialogsVisibleGetter
    @system.Action setDialogVisible

    public get visible() {
      return this.dialogsVisibleGetter[this.DialogKey]
    }

    @Emit('onClose')
    private handleClose() {
      if (!this.visible) {
          return
      }
      this.setDialogVisible({ key: this.DialogKey, visible: false })
    }

    public close() {
      this.setDialogVisible({ key: this.DialogKey, visible: false })
    }
  }
</script>
