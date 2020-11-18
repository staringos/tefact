<template>
  <div class="menu-list">
    <ArrTitle bordered>数据源列表
      <el-button size="small" icon="el-icon-plus" circle @click="handleDialogOpen()" />
    </ArrTitle>
    <el-table
      :data="dataSources"
      style="width: 100%">
      <el-table-column
        prop="name"
        label="名称"
        width="180">
      </el-table-column>
      <el-table-column
        prop="type"
        label="类型"
        width="180">
      </el-table-column>
      <el-table-column
        prop="address"
        label="地址">
      </el-table-column>
      <el-table-column
        prop="sort"
        label="操作"
        width="180">
        <template slot-scope="scope">
          <el-button type="default" size="small" round @click.stop="handleEdit(scope.row)">编辑</el-button>
          <el-button type="danger" size="small" round @click.stop="handleDelete(scope.row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog
      title="数据源编辑"
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
  import { Vue, Component } from 'nuxt-property-decorator'
  import { DataSource } from '~/services/common/entities/datasource'

  @Component
  export default class AppItem extends Vue {
    dataSources: DataSource[] = []
    dialogVisible: boolean = false
    form: DataSource | null = null

    handleCancel() {
      this.form = null
      this.dialogVisible = false
    }

    refresh() {

    }

    mounted() {
      this.refresh()
    }
  }
</script>
