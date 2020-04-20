<template>
  <div>
    <DialogX
      title="创建组织"
      :DialogKey="DialogKey"
      @onClose="handleDialogClose"
      ref="dialog"
      :show-close="false">
      <el-form :model="orgForm" status-icon :rules="rules" ref="orgForm" label-width="100px">
        <el-form-item label="组织名" prop="name">
          <el-input type="text" v-model="orgForm.name" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="组织ID" prop="unique_id">
          <el-input type="text" v-model="orgForm.unique_id" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="组织简介" prop="description">
          <el-input type="text" v-model="orgForm.description" autocomplete="off"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button type="default" size="small" @click="handleDialogClose">取消</el-button>
        <el-button type="primary" size="small" @click="handleCreateOrg">确定</el-button>
      </span>
    </DialogX>
    <el-dialog
      title="创建组织"
      :visible.sync="createOrgSuccess"
      width="30%"
      modal
    >
      <span>组织创建成功，是否立即邀请成员</span>
      <span slot="footer" class="dialog-footer">
          <el-button type="default" size="small" @click="createOrgSuccess = false">稍后处理</el-button>
          <el-button type="primary" size="small" @click="handleInvite">邀请成员</el-button>
        </span>
    </el-dialog>
  </div>
</template>
<style lang="scss">

</style>
<script lang="ts">
  import { Vue, Component, namespace } from 'nuxt-property-decorator'
  import { DefaultOrgParams } from '@arrplat/common'
  import { DialogX } from '@arrplat/ui'
  import { DIALOG_NAME } from '~/store/system'

  const org = namespace('org')
  const app = namespace('app')
  const system = namespace('system')

  @Component({
    components: { DialogX }
  })
  export default class AppItem extends Vue {
    DialogKey: string = DIALOG_NAME.CREATE_ORG

    orgForm = { ...DefaultOrgParams }
    createOrgSuccess:boolean = false

    @org.Action createOrg
    @app.Action getAllOrgs
    @system.Action setDialogVisible

    rules = {
      name: [{ required: true, message: '请输入组织名称', trigger: 'blur' }],
      unique_id: [{ required: true, message: '请输入组织唯一ID', trigger: 'blur' }],
      description: [{ required: false }]
    }

    async handleCreateOrg() {
      try {
        await new Promise((resolve, reject) => {
          (this.$refs['orgForm'] as HTMLFormElement).validate(async (valid) => valid ? resolve() : reject({}))
        })

        await this.createOrg(this.orgForm)
        this.getAllOrgs(1)
        this.$message.success('添加成功')
        this.handleDialogClose()
      } catch(e) {
        if (e.response) {
          this.$message.error(e.response.data.message)
        } else {
          this.$message.error('请输入正确的表单')
        }
      }
    }

    handleInvite() {
      this.createOrgSuccess = false
      this.$router.push('/plugins/org/staffs')
    }

    handleDialogClose() {
      (this.$refs.dialog as any).close()
      this.createOrgSuccess = true
      this.orgForm = { ...DefaultOrgParams }
    }
  }
</script>
