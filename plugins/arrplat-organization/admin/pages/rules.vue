<template>
  <ArrPanel title="角色权限管理" border>
    <ArrPanel style="min-width: 220px; width:220px;" headerButton="el-icon-plus" @on-header-button-click="() => openRoleDialog(false)" title="角色管理" :border="true" :header="true" :noPadding="true">
      <List style="margin-top: 20px;" v-bind:active.sync="currentRoleId" :list="allRoles">
        <div slot="right" slot-scope="data">
          <el-button type="text" icon="el-icon-edit" circle size="mini" @click="() => openRoleDialog(true, { ...data.data })"></el-button>
          <el-button class="color-red" style="margin-left: 1px;" type="text" icon="el-icon-delete" circle size="mini" @click="() => handleDeleteRole(data.data.id)"></el-button>
        </div>
      </List>
    </ArrPanel>

    <div class="role-setting-table">
      <div class="role-setting-tab">
        <el-tabs style="flex-grow: 1;" v-model="tabActive">
          <el-tab-pane label="角色成员" name="staff"></el-tab-pane>
          <el-tab-pane label="角色权限" name="auth"></el-tab-pane>
        </el-tabs>
      </div>
      <RoleStaffTable v-if="tabActive === 'staff'" :currentRoleId="currentRoleId" @onRefreshTable="refreshRolesStaff" :staffs="roleStaffs"></RoleStaffTable>
      <div v-if="tabActive === 'auth'">
        <SaveButton @onClick="handleAuthSave">保存</SaveButton>
        <el-tree
          class="clearfix"
          :data="treeAuth"
          show-checkbox
          node-key="id"
          ref="tree"
          :default-checked-keys="roleAuth"
          default-expand-all>
        </el-tree>
      </div>
    </div>
    <el-dialog
      :title="`${isEdit ? '修改' : '新增'}角色`"
      :visible.sync="dialogVisible"
      width="30%">
      <el-form label-width="100px">
        <el-form-item label="角色名称" prop="name">
          <el-input v-model="roleData.name"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="handleRoleModify">确 定</el-button>
      </span>
    </el-dialog>
  </ArrPanel>
</template>
<style lang="scss">
  .role-setting-table {
    width: 100%;
    padding-left: 20px;
    padding-right: 20px;
    flex-grow: 1;
    flex-shrink: 1;
    overflow: hidden;

    .role-setting-tab {
      display: flex;
      flex-direction: row;
    }
  }
</style>
<script lang="ts">
  import { Component, Vue, namespace, Watch } from 'nuxt-property-decorator'
  import _ from 'lodash'
  import { List, Confirm } from '@arrplat/ui'
  import RoleStaffTable from '../components/RoleStaffTable'
  import SaveButton from '../components/SaveButton'
  import { DefaultRole, Role, Staff, Auth } from '@arrplat/common'

  const org = namespace('org')
  const app = namespace('app')

  @Component({
    layout: 'plugin',
    components: {
      List, RoleStaffTable, SaveButton
    }
  })
  export default class Roles extends Vue {

    @org.Action getRoles
    @org.Action modifyRole
    @org.Action getRolesStaff
    @org.Action getRolesAuth
    @org.Action getAuth
    @org.Action deleteRole
    @org.Action saveRoleAuth

    @org.Getter allRoles
    @org.Getter allAuth
    @app.Getter currentOrg

    roleStaffs:Staff[] = []
    auth:Auth[] = []
    roleAuth:string[] = []

    roleData: Role = { ...DefaultRole }
    dialogVisible: boolean = false
    isEdit: boolean = false
    tabActive: string = 'staff'
    currentRoleId: string = '-1'

    defaultProps = {
      children: 'children',
      label: 'label'
    }

    get treeAuth() {
      const loop = (auth) => {
        const res:any = []

        auth.map(auth => {
          res.push({
            ...auth,
            label: auth.name,
            children: auth.children.length > 0 ? loop(auth.children) : []
          })
        })
        return res
      }

      return loop(this.allAuth)
    }

    handleAuthSave() {
      const checked = this.$refs.tree.getCheckedKeys()
      this.saveRoleAuth({ roleId: this.currentRoleId , orgId: this.currentOrg.id, auth: checked }).then(res => {
        if (res.status === 200) {
          this.roleAuth = checked
          return this.$message({ message: '更新成功', type: 'success' })
        }

        this.$message({ message: res.data.message, type: 'error' })
      })
    }

    handleDeleteRole(roleId) {
      Confirm.deleteConfirm(this, '角色', () => this.deleteRole({roleId, orgId: this.currentOrg.id}))
          .then(() => this.refreshPage())
    }

    openRoleDialog(isEdit, data) {
      this.isEdit = isEdit
      this.dialogVisible = true

      if (isEdit) {
        this.roleData = data
      }
    }

    async handleRoleModify() {
      const res = await this.modifyRole({ isEdit: this.isEdit, orgId: this.currentOrg.id, roleName: this.roleData.name, roleId: this.roleData.id })
      if(res.status === 200) {
        this.$message({ message: '更新成功', type: 'success' })
        this.dialogVisible = false
        return this.getRoles(this.currentOrg.id)
      }

      this.$message({ message: '更新失败', type: 'success' })
    }

    handleRoleSelect(id) {
      this.currentRoleId = id
    }

    @Watch('currentOrg')
    async onCurrentOrg() {
      if(!this.currentOrg) return
      this.refreshPage()
    }

    @Watch('currentRoleId')
    async onCurrentRoleChange() {
      if(!this.currentOrg) return

      if (this.tabActive === 'staff') {
        this.refreshRolesStaff()
      }

      if (this.tabActive === 'auth') {
        this.refreshAuth()
      }
    }

    @Watch('tabActive')
    onTabActiveChanged() {
      console.log('onTabActiveChanged')
      this.refreshTab()
    }

    async refreshPage() {
      // refresh roles
      const res = await this.getRoles(this.currentOrg.id)
      if (this.currentRoleId === '-1' || !_.find(res, { id: this.currentRoleId })) this.currentRoleId = res[0].id

      this.refreshTab()
    }

    refreshTab() {
      this.tabActive === 'staff' && this.refreshRolesStaff()
      this.tabActive === 'auth' && this.refreshAuth()
    }

    refreshAuth() {
      const pAll = this.getAuth(this.currentOrg.id)

      const pHas = this.getRolesAuth({ roleId: this.currentRoleId, orgId: this.currentOrg.id }).then(res => {
        this.roleAuth = res.data.data
        return this.roleAuth
      })

      Promise.all([pAll, pHas]).then(res => {
        console.log('auth res:', res)
      })
    }

    refreshRolesStaff() {
      this.getRolesStaff({ roleId: this.currentRoleId, orgId: this.currentOrg.id }).then(res => {
        this.roleStaffs = res.data.data
      })
    }

    created() {
      this.refreshPage()
    }
  }
</script>
