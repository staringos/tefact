<template>
  <DialogX title="创建轻应用" :DialogKey="DialogKey" ref="dialog">
    <el-form ref="form" :model="form" :rules="rules" label-width="80px">
      <el-form-item label="组织" required>
        <el-select v-model="form.org_id" placeholder="请选择组织">
          <el-option v-for="(item, i) in allOrgs" :key="item.id" :label="item.name" :value="item.id"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="应用名" required>
        <el-input v-model="form.title"></el-input>
      </el-form-item>
      <el-form-item label="应用介绍">
        <el-input type="textarea" v-model="form.description"></el-input>
      </el-form-item>
      <el-button type="primary" @click="handleSubmit">立即创建</el-button>
    </el-form>
  </DialogX>
</template>
<style lang="scss">

</style>
<script lang="ts">
  import { Vue, Component, namespace, Watch } from 'nuxt-property-decorator'
  import { DIALOG_NAME } from '~/store/system'
  import omitBy from 'lodash/omitBy'
  import isNull from 'lodash/isNull'

  const system = namespace('system')
  const app = namespace('app')

  const initForm = {
      org_id: null,
      title: null,
      description: null,
  }

  @Component
  export default class AppItem extends Vue {
    DialogKey: string = DIALOG_NAME.LIGHT_APP_MODIFY_DIALOG
    form = { ...initForm }

    @app.Getter allOrgs
    @app.Getter currentOrgIdGetter
    @app.Action lightAppAdd
    @system.Action setDialogVisible

    rules = {
      title: [{ required: true, message: '请输入名称', trigger: 'blur' }],
      description: [{ required: false }],
      org_id: [{ required: true, message: '请选择组织', trigger: 'blur' }],
    }

    @system.Getter dialogsVisibleGetter

    public get visible() {
      return this.dialogsVisibleGetter[this.DialogKey]
    }

    @Watch('visible')
    onVisibleChange() {
      if (this.visible && this.currentOrgIdGetter) {
        this.form.org_id = this.currentOrgIdGetter
      }
    }

    public async handleSubmit() {
      await new Promise((resolve, reject) =>
        (this.$refs['form'] as HTMLFormElement).validate(async (valid) => valid ? resolve() : reject({}))
      )

      const res = await this.lightAppAdd(omitBy(this.form, isNull))
      this.setDialogVisible({ key: this.DialogKey, visible: false })
      this.form = { ...initForm }
      this.$router.push(`/app/light/${res.data.data.id}`)
    }
  }
</script>
