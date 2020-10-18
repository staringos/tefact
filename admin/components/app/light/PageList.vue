<template>
  <div>
    <ArrTitle bordered>页面列表
      <el-button size="small" icon="el-icon-plus" @click="handleEdit()" circle />
    </ArrTitle>
    <el-table
      :data="pages"
      @row-click="handleRowClick"
      style="width: 100%">
      <el-table-column
        prop="title"
        label="页面名"
        width="180">
      </el-table-column>
      <el-table-column
        prop="key"
        label="KEY"
        width="180">
      </el-table-column>
      <el-table-column
        prop="direction"
        label="页面方向">
      </el-table-column>
      <el-table-column
        prop="sort"
        label="操作"
        width="180">
        <template slot-scope="scope">
          <el-button type="default" size="small" round @click.stop="handleRowClick(scope.row)">编辑</el-button>
<!--          <el-button type="default" size="small" round @click.stop="handleEdit(scope.row)">编辑</el-button>-->
          <el-button type="danger" size="small" round @click.stop="handleDelete(scope.row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog
      title="页面编辑"
      :visible.sync="dialogVisible"
      :before-close="handleCancel"
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
        <el-button v-if="isEdit" type="warning" @click="handleRowClick({ id: form.id })">编辑器</el-button>
        <el-button @click="dialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="handleSave()">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>
<style lang="scss">

</style>
<script lang="ts">
  import { Vue, Component, Prop, namespace, Emit } from 'nuxt-property-decorator'
  import PageSectionList from './PageSectionList.vue'
  import { Confirm } from '~/components/ui'
  import Constants from '~/services/common/constants'

  const app = namespace('app')

  @Component({
    components: { PageSectionList }
  })
  export default class PageList extends Vue {
    @Prop() pages
    @Prop() entities
    @Prop() appId
    @Prop() onChange
    dialogVisible = false
    isEdit = false
    form = { ...Constants.entities.DefaultPage } as any
    PageDirection = Constants.entities.PageDirection

    @app.Action addPage
    @app.Action modifyPage
    @app.Action deletePage

    handleRowClick(row) {
      this.$router.push(`/app/light/${this.appId}/${row.id}/editor`)
    }

    @Emit('refresh')
    async handleSave() {
      const data = { ...this.form }
      delete data.sections
      data.app_id = this.appId

      let res
      if (this.isEdit) res = await this.modifyPage(data)
      else res = await this.addPage(data)

      if (res.status === 200) {
        this.$emit('refresh')
        this.$message({ message: '操作成功', type: 'success' })
        return this.handleCancel()
      }

      this.$message({ message: '操作失败，请重试', type: 'error' })
    }

    handleCancel() {
      this.dialogVisible = false
      this.isEdit = false
      this.form = { ...Constants.entities.DefaultPage }
    }

    handleEdit(item) {
      if (item) {
        this.form = item
        this.isEdit = true
      }

      this.dialogVisible = true
    }

    async handleDelete(item) {
      Confirm.deleteConfirm(this, '页面', () => this.deletePage(item.id))
        .then(() => {
          this.$emit('refresh')
          this.handleCancel()
        })
    }

    mounted() {
    }
  }
</script>
