<template>
  <div>
    <ArrTitle bordered>页面列表
      <el-button size="small" icon="el-icon-plus" @click="handleEdit()" circle />
    </ArrTitle>
    <el-table
      :data="pages"
      @row-click="handleRowClick"
      size="small"
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
    <PageModifyDialog :isEdit="isEdit" :form="form" :appId="appId" :dialogVisible="dialogVisible" @cancel="handleCancel" @modifed="handleEdit" @refresh="$emit('refresh')" />
  </div>
</template>
<style lang="scss">

</style>
<script lang="ts">
  import { Vue, Component, Prop, namespace, Emit } from 'nuxt-property-decorator'
  import PageSectionList from './PageSectionList.vue'
  import { Confirm } from '~/components/ui'
  import Constants from '~/services/common/constants'
  import PageModifyDialog from "~/components/app/light/page/PageModifyDialog.vue"

  const app = namespace('app')

  @Component({
    components: { PageModifyDialog, PageSectionList }
  })
  export default class PageList extends Vue {
    @Prop() pages
    @Prop() entities
    @Prop() appId
    @Prop() onChange
    dialogVisible = false
    isEdit = false
    form = { ...Constants.entities.DefaultPage } as any

    @app.Action deletePage

    handleRowClick(row) {
      this.$router.push(`/app/light/${this.appId}/${row.id}/editor`)
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
  }
</script>
