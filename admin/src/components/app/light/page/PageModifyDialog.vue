<template>
  <el-dialog
    title="页面编辑"
    :visible.sync="dialogVisible"
    :before-close="() => $emit('cancel')"
    :close-on-click-modal="false"
    :close-on-press-escape="false"
    width="30%">
    <el-form label-width="80px" :model="form">
      <el-form-item label="标题">
        <el-input v-model="form.title"></el-input>
      </el-form-item>
      <el-form-item label="页面方向">
        <el-select v-model="form.direction" placeholder="请选择">
          <el-option
            v-for="item in PageDirection"
            :key="item.key"
            :label="item.value"
            :value="item.key">
          </el-option>
        </el-select>
      </el-form-item>
    </el-form>
    <span slot="footer" class="dialog-footer">
        <el-button @click="$emit('cancel')">取 消</el-button>
        <el-button type="primary" @click="handleSave()">确 定</el-button>
      </span>
  </el-dialog>
</template>
<style lang="scss">

</style>
<script lang="ts">
import { Vue, Component, Emit, Prop, namespace } from 'nuxt-property-decorator'
import Constants from "~/services/common/constants"

const app = namespace('app')

@Component
export default class PageModifyDialog extends Vue {
  @Prop(Object) form
  @Prop(Boolean) isEdit
  @Prop(Boolean) dialogVisible
  @Prop(String) appId

  @app.Action addPage
  @app.Action modifyPage

  PageDirection = Constants.entities.PageDirection

  @Emit('refresh')
  async handleSave() {
    const data = { ...this.form }
    const that = this as any
    delete data.sections
    data.app_id = this.appId

    let res
    if (this.isEdit) res = await this.modifyPage(data)
    else res = await this.addPage(data)

    if (res.status === 200) {
      this.$emit('refresh')
      that.$message({ message: '操作成功', type: 'success' })
      return this.$emit('cancel')
    }

    that.$message({ message: '操作失败，请重试', type: 'error' })
  }
}
</script>
