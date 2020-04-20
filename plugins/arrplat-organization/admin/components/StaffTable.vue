<template>
  <el-table
    :data="allStaffs"
    stripe>
    <el-table-column
      prop="date"
      label="成员"
      width="220">
      <template slot-scope="scope">
        <div class="staff-avatar">
          <el-avatar style="width: 40px; margin-right: 10px;" :src="scope.row.user.user_info.head_url"></el-avatar>
          <div>
            <h2>{{scope.row.user.nickname}}</h2>
            <span>{{scope.row.user.user_info.signature}}</span>
          </div>
        </div>
      </template>
    </el-table-column>
    <el-table-column
      prop="user.phone"
      label="手机号">
    </el-table-column>
    <el-table-column
      prop="user.gender"
      label="性别"
      width="50">
      <template slot-scope="scope">
        <span>{{scope.row.user.gender === 1 ? '男' : '女'}}</span>
      </template>
    </el-table-column>
    <el-table-column
      prop="name"
      label="部门">
      <template slot-scope="scope">
        <span v-for="department in scope.row.org_department_staff">{{department.org_department.name}}</span>
      </template>
    </el-table-column>
    <el-table-column
      prop="parent_superior.user.nickname"
      label="直属上级">
    </el-table-column>
    <el-table-column
      prop="job_title"
      label="岗位">
    </el-table-column>
    <el-table-column
      prop="address"
      label="角色">
      <template>
        <el-tag type="info">标签三</el-tag>
      </template>
    </el-table-column>
    <el-table-column
      prop="option"
      label="操作">
      <template slot-scope="scope">
        <el-button v-if="!customOption" type="primary" @click="openStaffEditDialog(true, scope.row)" icon="el-icon-edit" circle></el-button>
        <el-button v-if="!customOption" type="danger" @click="() => handleRemoveStaff(scope.row.id)" icon="el-icon-delete" circle></el-button>
        <slot name="option" :row="scope.row"></slot>
      </template>
    </el-table-column>
  </el-table>
</template>
<style lang="scss">
  .staff-avatar {
    display: flex;
    align-items: center;

    h2 {
      font-weight: 700;
    }
  }
</style>
<script lang="ts">
  import { Component, Vue, namespace, Watch, Prop } from 'nuxt-property-decorator'
  import { Confirm } from '@arrplat/ui'
  const org = namespace('org')
  const app = namespace('app')

  @Component({})
  export default class MemberTable extends Vue {

    @Prop([Array]) allStaffs
    @Prop([Function]) openStaffEditDialog
    @Prop([Boolean]) customOption
    @org.Action removeStaff
    @app.Getter currentOrg

    handleRemoveStaff(staffId) {
      Confirm.deleteConfirm(this, '成员', () => this.removeStaff({ orgId: this.currentOrg.id, staffId }))
        .then(() => this.$emit('onRefreshTable'))
    }
  }
</script>
