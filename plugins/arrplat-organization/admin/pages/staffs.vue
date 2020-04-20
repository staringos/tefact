<template>
  <ArrPanel title="成员管理" border>
    <DepartmentTree @on-department-select="handleDepartmentChange" />
    <div class="member-table">
      <div class="search-bar">
        <el-input
          placeholder="请输入内容"
          prefix-icon="el-icon-search"
          v-model="searchContent"></el-input>
        <el-button type="primary" @click="() => openStaffEditDialog(false)">新建员工</el-button>
      </div>
      <StaffTable @onRefreshTable="refreshTable" :allStaffs="allStaffs" :openStaffEditDialog="openStaffEditDialog" />
    </div>

    <StaffEditor :staff="staff" :isEdit="isEdit" :dialogVisible="dialogVisible" @onChange="handleDialogChanged" @onCancel="handleCancel" />
  </ArrPanel>
</template>
<style lang="scss">
  .member-table {
    padding-left: 20px;
    flex: 1;
  }

  .search-bar {
    display: flex;

    .el-button {
      margin-left: 20px;
    }
  }
</style>
<script lang="ts">
  import DepartmentTree from '../components/DepartmentTree'
  import { Component, Vue, namespace, Watch } from 'nuxt-property-decorator'
  import StaffTable from '../components/StaffTable'
  import StaffEditor from '../components/StaffEditor'
  import { Staff, DefaultStaff } from '@arrplat/common'

  const app = namespace('app')
  const org = namespace('org')

  @Component({
    layout: 'plugin',
    components: {
      StaffTable,
      StaffEditor,
      DepartmentTree
    }
  })
  export default class StaffPage extends Vue {
    searchContent: string = ''
    allStaffs: any[] = []
    currentDepartmentId: string = '-1'
    isEdit:boolean = false
    dialogVisible:boolean = false
    staff:Staff = { ...DefaultStaff }

    handleCancel() {
      this.dialogVisible = false
    }

    handleDepartmentChange (id) {
      this.currentDepartmentId = id
      this.refreshTable()
    }

    mounted() {
      this.refreshTable()
    }

    @app.Getter currentOrg
    @org.Action getStaffs

    @Watch('currentOrg', { immediate: true, deep: true })
    onCurrentOrg() {
      this.refreshTable()
    }

    @org.Action getRoles

    openStaffEditDialog(isEdit, staff) {
      console.log('[openStaffEditDialog] isEdit:', isEdit, 'staff:', staff)
      this.dialogVisible = true
      this.getRoles(this.currentOrg.id)

      if (isEdit) {
        this.isEdit = true
        this.staff = staff
      }
    }

    handleDialogChanged() {
      this.refreshTable()
      this.dialogVisible = false
    }

    async refreshTable() {
      if (!this.currentOrg) {
        return
      }
      this.allStaffs = await this.getStaffs({ orgId: this.currentOrg.id, departmentId: this.currentDepartmentId })
    }
  }
</script>
