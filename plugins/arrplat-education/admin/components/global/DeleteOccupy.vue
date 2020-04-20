<!-- 去除占用问询弹窗 -->
<template>
  <el-dialog
    title="提示"
    :visible.sync="dialogDeleteZy"
    width="30%"
    :before-close="handleZyClose">
    <span>去除占用？</span>
    <span slot="footer" class="dialog-footer">
      <el-button @click="handleZyClose">取 消</el-button>
      <el-button type="primary" @click="handleZyTrue">确 定</el-button>
    </span>
  </el-dialog>
</template>
<style lang="scss">

</style>
<script lang="ts">
  import { Vue, Component, Prop, Watch, Emit, namespace } from 'nuxt-property-decorator'
  const edu = namespace('education')
  @Component({})
  export default class DeleteOccupy extends Vue {
    @edu.Action curriculum
    @Prop() dialogDeleteZy: boolean

    // 删除占用弹窗关闭
    handleZyClose(){
      this.$emit('delete-occupy','close');
    }
    // 删除占用弹窗确定
    handleZyTrue(){
      this.$emit('delete-occupy','true');
    }
  }
</script>
