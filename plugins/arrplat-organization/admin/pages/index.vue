<template>
  <ArrPanel title="组织详情" border>
    <div class="org-details">
      <AvatarUploader :size="122" :link="form.head_url" :actionUrl="uploadUrl" @onChange="handleAvatarChanged" />
      <el-form class="form" label-width="80px" :model="form">
        <el-form-item label=" 组织名称">
          <el-input v-model="form.name"></el-input>
        </el-form-item>
        <el-form-item label="地址">
          <el-input v-model="form.address"></el-input>
        </el-form-item>
        <el-form-item label="官网">
          <el-input v-model="form.website"></el-input>
        </el-form-item>
        <el-form-item label="简介">
          <el-input v-model="form.description"></el-input>
        </el-form-item>
      </el-form>
      <el-button type="primary" style="width: 200px;" @click="handleSubmit">保存</el-button>
    </div>
  </ArrPanel>
</template>
<style lang="scss" scoped>
  .org-details {
    min-width: 50%;
    max-width: 500px;
    display: flex;
    align-items: center;
    flex-direction: column;

    .form {
      width: 340px;
      margin-top: 30px;
    }
  }
</style>
<script lang="ts">
  import { Component, Vue, namespace, Watch, Emit } from 'nuxt-property-decorator'
  // import { Panel, AvatarUploader } from '@arrplat/ui'

  const app = namespace('app')
  const system = namespace('system')
  const org = namespace('org')

  @Component({
    layout: 'plugin'
  })
  export default class Plugin extends Vue {

    @app.Action getAllOrgs
    @app.Getter currentOrg
    @system.Getter uploadUrl
    @org.Action modifyOrg

    form = {
      id: '',
      head_url: '',
      name: '',
      address: '',
      website: '',
      description: ''
    }

    @Watch('currentOrg')
    onCurrentOrgChange() {
      this.refreshForm()
    }

    refreshForm() {
      this.form = { ...this.currentOrg }
    }

    handleAvatarChanged(url) {
      this.form.head_url = url
    }

    async handleSubmit() {
      try {
        await this.modifyOrg(this.form)
        this.getAllOrgs()
        this.$message({ message: '操作成功', type: 'success' })
      } catch(e) {
        this.$message({ message: e.response.data.message, type: 'error' })
      }
    }

    mounted() {
      this.refreshForm()
    }
  }
</script>
