<template>
  <el-dialog
    title="个人详情"
    :visible="userDetailsVisibleGetter"
    width="40%"
    :close-on-click-modal="false"
    :close-on-press-escape="false"
    :before-close="handleClose">
    <div v-if="currentUser">
      <div class="section section-base-info">
        <div class="user-avatar">
          <el-avatar :size="91" :src="currentUser.user_info.head_url"></el-avatar>
        </div>
        <div class="user-details">
          <ArrTitle size="h2">{{currentUser.nickname}}</ArrTitle>
          <p>{{currentUser.user_info.signature}}</p>
          <AttributeList :attributes="attributes"/>
        </div>
      </div>
      <div class="section">
        <ArrTitle>组织列表</ArrTitle>
        <el-table
          :data="allOrgs"
          style="width: 100%">
          <el-table-column
            prop="name"
            label="组织">
          </el-table-column>
          <el-table-column
            prop="name"
            label="部门"
            width="180">
            <template slot-scope="scope" v-if="scope.row.staff_info">
              <el-tag :key="i" v-for="(department, i) in scope.row.staff_info.org_department" type="info">{{department.name}}</el-tag>
            </template>
          </el-table-column>
          <el-table-column
            prop="staff_info.job_title"
            label="职位">
          </el-table-column>
          <el-table-column
            prop="option"
            label="操作">
            <template slot-scope="scope">
              <el-button type="text" @click="() => handleExitOrg(scope.row.id)">退出组织</el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </div>
    <span slot="footer" class="dialog-footer">
      <el-button @click="handleClose">关 闭</el-button>
      <el-button type="primary" @click="showModifyUserDetails">修改个人信息</el-button>
    </span>
  </el-dialog>
</template>
<style lang="scss">
  .section-base-info {
    display: flex;
    margin-bottom: 30px;

    .user-avatar {
      flex: 1;
      width: 100%;
      justify-content: center;
      align-items: center;
      display: flex;
    }

    .user-details {
      display: flex;
      flex: 2;
      flex-direction: column;
    }
  }
</style>
<script lang="ts">
  import { Component, Vue, namespace, Emit, Watch } from 'nuxt-property-decorator'
  import { Confirm } from '@arrplat/ui'
  import { DIALOG_NAME } from '../../store/system'

  const user = namespace('user')
  const app = namespace('app')
  const system = namespace('system')

  @Component
  export default class UserDetailDialog extends Vue {
    @user.Action toggleUserDetailsDialog
    @user.Action exitOrg
    @user.Getter userDetailsVisibleGetter
    @user.Getter currentUser
    @app.Getter allOrgs
    @app.Action getAllOrgs
    @system.Action setDialogVisible

    get attributes() {
      return [{
        key: '手机号',
        value: this.currentUser.phone
      }, {
        key: '邮 箱',
        value: this.currentUser.user_info.email
      }, {
        key: '性 别',
        value: this.currentUser.user_info.gender === 1 ? '男':'女'
      }]
    }

    handleClose() {
      this.toggleUserDetailsDialog(false)
    }

    handleExitOrg(id) {
      Confirm.deleteConfirm(this, '组织', () => this.exitOrg(id), '退出')
        .then(() => this.getAllOrgs(1))
    }

    showModifyUserDetails() {
      this.setDialogVisible({ key: DIALOG_NAME.USER_MODIFY_DIALOG, visible: true })
    }

    @Watch('userDetailsVisibleGetter')
    visibleChanged() {
      if (this.userDetailsVisibleGetter) {
        this.getAllOrgs(1)
      }
    }
  }
</script>
