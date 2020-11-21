<template>
  <el-dialog
    title="Tefact 低代码平台"
    :visible="info && !auth"
    width="80%"
    :before-close="handleClose"
    :show-close="false"
  >
    <span>分享页面验证</span>

    <el-input v-model="pwd" type="password" placeholder="请输入密码"></el-input>
    <span slot="footer" class="dialog-footer">
    <el-button type="primary" @click="handleConfirm">确 定</el-button>
  </span>
  </el-dialog>
</template>
<style lang="scss">

</style>
<script lang="ts">
import { Vue, Component, Prop } from 'nuxt-property-decorator'
import { service } from '~/utils'

@Component
export default class RequestPasswordDialog extends Vue {
  @Prop(Boolean) auth
  @Prop(Object) info

  pwd: string = ""

  handleClose() {}

  async handleConfirm() {
    const that = (this as any);
    if (!this.pwd || this.pwd.trim() === "") {
      return that.$message({ message: '请输入密码', type: 'error' })
    }

    if (this.pwd.length !== 6) {
      return that.$message({ message: '密码格式不正确', type: 'error' })
    }

    const res = await service.app.getSharePageDetails(this.info.key, this.pwd)

    if (res && res.data) {
      return this.$emit("authed", res.data.data)
    }
    return that.$message({ message: '密码校验失败', type: 'error' })
  }
}
</script>
