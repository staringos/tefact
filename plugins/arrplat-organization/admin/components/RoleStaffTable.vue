<template>
  <div class="role-staff-table">
    <SaveButton @onClick="showModifyStaffDialog">添加人员</SaveButton>
    <StaffTable :customOption="true" @onRefreshTable="handleRefreshTable" :allStaffs="staffs">
      <div slot="option" slot-scope="scope">
        <el-button type="danger" @click="() => handleRemoveStaff(scope.row.id)" icon="el-icon-delete" circle></el-button>
      </div>
    </StaffTable>

    <el-dialog
      :title="`关联人员`"
      :visible.sync="dialogStaffVisible"
      width="30%">
      <el-form label-width="100px">
        <el-select :loading="dialogSelectLoading" v-model="selectIds" multiple placeholder="请选择">
          <el-option
            v-for="item in allStaffs"
            :key="item.id"
            :label="item.user.nickname"
            :value="item.id">
            <span style="float: left">{{ item.user.nickname }}</span>
            <span style="float: right; color: #8492a6; font-size: 13px">{{ item.value }}</span>
          </el-option>
        </el-select>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="handleModifyStaff">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>
<style lang="scss">
  .role-staff-table {
  }
</style>
<script lang="ts">
  import { Vue, Component, Prop, namespace, Watch, Emit } from 'nuxt-property-decorator'
  import StaffTable from './StaffTable'
  import SaveButton from './SaveButton'
  import { Confirm } from '@arrplat/ui'
  import _ from 'lodash'

  const org = namespace('org')
  const app = namespace('app')

  @Component({
    components: {
      StaffTable, SaveButton
    }
  })
  export default class RoleStaffTable extends Vue {
    dialogStaffVisible: boolean = false
    dialogSelectLoading: boolean = false

    @Prop([String]) currentRoleId
    @Prop([Array]) staffs
    @Prop([Array]) refreshTables

    @org.Action deleteRoleStaff
    @org.Action getStaffs
    @org.Action saveRoleStaff
    @org.Getter allStaffs
    @app.Getter currentOrg
    @app.Getter currentOrgIdGetter
    @app.Getter currentOrgIdGetter

    selectIds:string[] = []

    @Emit('onRefreshTable')
    handleRefreshTable(data) {
      return data
    }

    handleRemoveStaff(id) {
      Confirm.deleteConfirm(this, '成员', () => this.deleteRoleStaff({ orgId: this.currentOrg.id, roleId: this.currentRoleId, staffId: id }))
        .then(() => this.$emit('onRefreshTable'))
    }

    @Emit('onRefreshTable')
    async handleModifyStaff() {
      const res = await this.saveRoleStaff({ roleId: this.currentRoleId, orgId: this.currentOrg.id, staffIds: this.selectIds })
      if (res.status === 200) {
        this.$message({ message: '修改成功', type: 'success' })
        this.dialogStaffVisible = false
        return res
      }

      this.$message({ message: res.data.message, type: 'success' })
    }

    showModifyStaffDialog() {
      this.refreshAllStaff()
      this.selectIds = this.staffs.map(staff => staff.id)
      this.dialogStaffVisible = true
    }

    async refreshAllStaff() {
      this.dialogSelectLoading = true
      if (!this.currentOrgIdGetter) return
      await this.getStaffs({ orgId: this.currentOrgIdGetter, departmentId: '-1' })
      this.dialogSelectLoading = false
    }
  }
</script>
