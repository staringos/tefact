<template>
  <DialogX title="修改个人信息" :DialogKey="DialogKey" ref="dialog">
    <div class="user-avatar">
      <AvatarUploader :size="122" :link="userForm.head_url" :actionUrl="uploadUrl" @onChange="handleAvatarChanged" />
    </div>
    <el-form v-if="currentUser" :model="userForm" status-icon :rules="rules" ref="userForm" label-width="100px">
      <el-form-item label="*手机号" prop="phone">
        <el-input type="text" v-model="currentUser.phone" disabled autocomplete="off"></el-input>
      </el-form-item>
      <el-form-item label="名称" prop="nickname">
        <el-input type="text" v-model="userForm.nickname" autocomplete="off"></el-input>
      </el-form-item>
      <el-form-item label="简介" prop="signature">
        <el-input type="text" v-model="userForm.signature"></el-input>
      </el-form-item>
      <el-form-item label="邮箱" prop="email">
        <el-input type="text" v-model="userForm.email" autocomplete="off"></el-input>
      </el-form-item>
      <el-form-item label="性别" prop="gender">
        <el-radio v-model="userForm.gender" :label="1">男</el-radio>
        <el-radio v-model="userForm.gender" :label="0">女</el-radio>
      </el-form-item>
      <el-form-item>
        <el-button @click="handleClose">取 消</el-button>
        <el-button type="primary" @click="handleSubmit">保 存</el-button>
      </el-form-item>
    </el-form>
  </DialogX>
</template>
<style lang="scss">
  .user-avatar {
    width: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    padding-bottom: 30px;
  }
</style>
<script lang="ts">
  import { Component, Vue, namespace, Emit, Watch } from 'nuxt-property-decorator'
  import { DIALOG_NAME } from '~/store/system'
  import { DialogX } from '@arrplat/ui'
  import { DefaultUserParams, UserParams } from '@arrplat/common'

  const system = namespace('system')
  const user = namespace('user')

  @Component({
    components: { DialogX }
  })
  export default class UserModifyDialog extends Vue {
    DialogKey: string = DIALOG_NAME.USER_MODIFY_DIALOG
    userForm?: UserParams = { ...DefaultUserParams }

    rules = {
      nickname: [{ required: true, message: '请输入名称', trigger: 'blur' }],
      signature: [{ required: false }]
    }

    @user.Getter currentUser
    @user.Action editUser
    @user.Action refreshUserDetails
    @system.Getter dialogsVisibleGetter
    @system.Getter uploadUrl

    public get visible() {
      return this.dialogsVisibleGetter[this.DialogKey]
    }

    handleAvatarChanged(url) {
      this.userForm.head_url = url
    }

    @Watch('visible')
    onVisibleChange() {
      if (this.visible) {
        this.userForm = {
          head_url: this.currentUser.head_url || '',
          nickname: this.currentUser.nickname || '',
          signature: this.currentUser.user_info.signature || '',
          email: this.currentUser.user_info.email,
          gender: this.currentUser.user_info.gender || 1
        }
      }
    }

    async handleSubmit() {
      try {
        await new Promise((resolve, reject) => {
            (this.$refs['userForm'] as HTMLFormElement).validate(async (valid) => valid ? resolve() : reject({}))
        })

        const res = await this.editUser(this.userForm)
        if (res.status === 200) {
          this.refreshUserDetails()
          this.$message({ message: '修改成功', type: 'success' })
          this.handleClose()
        }
      } catch(e) {
        if (e.response) {
          this.$message({ message: e.response.data.message, type: 'error' })
        }
      }
    }

    handleClose() {
      (this.$refs.dialog as any).handleClose()
    }
  }
</script>
