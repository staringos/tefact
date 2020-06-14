<template>
  <el-dialog
    :title="`${isEdit ? '修改' : '新增'}员工`"
    :visible="dialogVisible"
    :close="handleCancel"
    width="30%">
    <el-form label-width="100px">
      <el-form-item label="手机号*" prop="name" disabled="isEdit"><el-input v-model="entity.phone"></el-input></el-form-item>
      <el-form-item label="部门" prop="name">
        <el-tree
          class="department-tree"
          :data="allDepartment"
          show-checkbox
          ref="departmentTree"
          node-key="id"
          default-expand-all></el-tree>
      </el-form-item>
      <el-form-item label="岗位" prop="name"><el-input v-model="entity.job_title"></el-input></el-form-item>
      <el-form-item label="直属上级*" prop="name">
        <el-select v-model="entity.superior_id" placeholder="请选择">
          <el-option
            v-for="item in allStaffs"
            :key="item.id"
            :label="`${item.user.nickname} - ${item.job_title}`"
            :value="item.id">
          </el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="角色" prop="name">
        <el-select v-model="entity.role_id_list" multiple placeholder="请选择">
          <el-option
            v-for="item in allRoles"
            :key="item.id"
            :label="item.name"
            :value="item.id">
          </el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="状态" prop="name">
        <el-switch
          style="display: block"
          v-model="entity.is_able"
          active-text="启用"
          inactive-text="停用"
          :active-value="1"
          :inactive-value="0">
        </el-switch>
      </el-form-item>

    </el-form>
    <span slot="footer" class="dialog-footer">
      <el-button @click="handleCancel">取 消</el-button>
      <el-button type="primary" @click="handleStaffAdd">确 定</el-button>
    </span>
  </el-dialog>
</template>
<script lang="ts">
  import { Component, Vue, namespace, Prop, Watch, Emit } from 'nuxt-property-decorator'
  import { StaffParams, DefaultStaff } from '~/services/common'
  import _ from 'lodash'

  const org = namespace('org')
  const app = namespace('app')

  @Component({})
  export default class StaffEditor extends Vue {
    entity: StaffParams = { is_able: 1 } as StaffParams

    @app.Getter currentOrg
    @org.Getter allRoles
    @org.Getter allDepartment
    @org.Getter allStaffs
    @org.Action addStaff
    @org.Action modifyStaff

    @Prop([Boolean]) isEdit
    @Prop([Object]) staff
    @Prop([Boolean]) dialogVisible

    @Emit('onCancel')
    handleCancel() {
      return
    }

    @Watch('dialogVisible')
    handleVisible() {
      this.$nextTick(() => {
        if (this.dialogVisible)
          (this.$refs.departmentTree as any).setCheckedKeys(this.entity.department_id_list)
      })
    }

    @Watch('staff')
    onStaffChange() {
      const entity = _.cloneDeep(this.staff)
      entity.phone = entity.user.phone

      if (entity.org_department && entity.org_department.length > 0)
        entity.department_id_list = entity.org_department.map(d => d.id)

      entity.superior_id = entity.parent_superior ? entity.parent_superior.id : null

      delete entity.user
      delete entity.org_department

      this.entity = entity
    }

    async handleStaffAdd() {
      const that = (this as any)
      if (!this.entity.phone || this.entity.phone.length < 1) {
        return that.$message({ message: '请输入手机号', type: 'error' })
      }

      if (!this.entity.superior_id) {
        return that.$message({ message: '请选择上级', type: 'error' })
      }

      const orgDepartment = (this.$refs.departmentTree as any).getCheckedKeys()
      const data = { ...this.entity, department_id_list: orgDepartment }

      try {
        if (this.isEdit)
          await this.modifyStaff({ orgId: this.currentOrg.id, data, id: this.entity.id })
        else
          await this.addStaff({ orgId: this.currentOrg.id, data })

        this.$emit('onChange')
        that.$message({ message: '操作成功', type: 'success' })
      } catch(e) {
        if (e.response)
          that.$message({ message: e.response.data.message, type: 'error' })
      }
    }
  }
</script>
