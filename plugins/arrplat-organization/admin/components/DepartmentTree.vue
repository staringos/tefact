<template>
  <ArrPanel style="min-width: 220px; max-width: 220px; width:220px;" headerButton="el-icon-plus" @on-header-button-click="() => openDepartmentDialog(false)" title="部门管理" :border="true" :header="true">
    <el-tree
      class="department-tree"
      :data="allDepartment"
      show-checkbox
      node-key="id"
      @node-click="handleNodeClick"
      default-expand-all>
      <span class="tree-operations" slot-scope="{ node, data }">
        <span>{{ node.label }}</span>
        <span class="btns">
          <el-button type="text" icon="el-icon-edit" circle size="mini" @click="() => openDepartmentDialog(true, node, data)"></el-button>
          <el-button class="color-red" type="text" icon="el-icon-delete" circle size="mini" @click="() => handleDeleteDepartment(node, data)"></el-button>
        </span>
      </span>
    </el-tree>

    <el-dialog
      :title="`${isEdit ? '修改' : '新增'}部门`"
      :visible.sync="dialogVisible"
      width="30%">
      <el-form label-width="100px">
        <el-form-item label="部门名称" prop="name">
          <el-input v-model="form.name" />
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="hideDialog">取 消</el-button>
        <el-button type="primary" @click="handleDepartmentAdd">确 定</el-button>
      </span>
    </el-dialog>
  </ArrPanel>
</template>
<style lang="scss">
  .department-tree {
    overflow: auto;
    width: 100%;

    .el-tree-node__content {
      .is-current {
        .btns {
          display: block !important;
        }
      }
    }

    .tree-operations {
      width: 100%;

      .btns {
        text-align: right;
        float: right;
        display: none;

        .el-button {
          margin: 0;
        }
      }

      &:hover {
        .btns {
          display: block;
        }
      }
    }
  }
</style>
<script lang="ts">
  import { Component, Vue, namespace, Watch, Emit } from 'nuxt-property-decorator'
  import { Confirm } from '@arrplat/ui'
  import * as constants from '../utils/constant'

  const org = namespace('org')
  const app = namespace('app')

  @Component
  export default class DepartmentTree extends Vue {
    dialogVisible: boolean = false
    isEdit: boolean = false
    currentDepartment: any = {}
    form: any = { ...constants.DefaultDepartment }

    @org.Action getCurrentDepartment
    @org.Action departmentModifier
    @org.Action deleteDepartment
    @app.Getter currentOrg
    @org.Getter allDepartment

    hideDialog() {
      this.dialogVisible = false
    }

    async handleDeleteDepartment(data) {
      Confirm.deleteConfirm(this, '部门', () => this.deleteDepartment({ isEdit: this.isEdit, orgId: this.currentOrg.id, departmentId: data.data.id }))
          .then(() => this.getCurrentDepartment(this.currentOrg.id))
    }

    async handleDepartmentAdd() {
      if (!this.currentDepartment.id)
        this.currentDepartment.id = this.allDepartment[0].id

      console.log('this.currentDepartment.name:', this.form.name)
      const params = { orgId: this.currentOrg.id, departmentName: this.form.name } as any
      if (this.isEdit) params.id = this.form.id
      else params.parentDepartmentId = this.currentDepartment.id

      console.log('params:', params)
      const res = await this.departmentModifier(params)

      if (res.status !== 200)
        return (this as any).$message({ message: res.data.message, type: 'warning' })

      (this as any).$message({ message: '添加成功', type: 'success' })

      this.getCurrentDepartment(this.currentOrg.id)
      this.dialogVisible = false
      this.form = { ...constants.DefaultDepartment }
    }

    openDepartmentDialog(isEdit, node, data) {
      console.log('click ??', isEdit, node, data)
      this.dialogVisible = true
      this.isEdit = isEdit

      if (isEdit) {
        this.form = { name: data.label, id: data.id } as any
      }
    }

    @Watch('currentOrg')
    onCurrentOrgChange() {
      if(!this.currentOrg) return
      this.getCurrentDepartment(this.currentOrg.id)
    }

    @Emit('on-department-select')
    handleNodeClick(e) {
      this.currentDepartment = e
      return this.currentDepartment.id
    }

    mounted() {
      if(!this.currentOrg) return
      this.getCurrentDepartment(this.currentOrg.id)
    }
  }
</script>
