<template>
  <el-popconfirm
    class="app-toggle-btn"
    :confirmButtonText="item.is_install ? '移除' : '添加'"
    cancelButtonText='不用了'
    icon="el-icon-info"
    iconColor="red"
    :title="`确定要${item.is_install ? '移除' : '添加'}应用吗`"
    @onConfirm="handleToggleApp"
  >
    <el-button slot="reference" :type="type || 'primary'" round>{{item.is_install ? '移除' : '添加'}}</el-button>
  </el-popconfirm>
</template>
<style lang="scss">
  .app-toggle-btn {
    flex: 1;
    text-align: center;
  }
</style>
<script lang="ts">
  import { Vue, Component, namespace, Prop, Emit } from 'nuxt-property-decorator'
  import { Application } from '@arrplat/common'

  const app = namespace('app')

  @Component
  export default class AppToggleBtn extends Vue {
    @Prop(Application) item: Application
    @Prop(String) type?: string

    @app.Action toggleApp
    @app.Getter currentOrg

    @Emit('onChange')
    async handleToggleApp() {
      const res = await this.toggleApp({ appId: this.item.id, orgId: this.currentOrg.id, isAdd: this.item.is_install === 1 ? 0 : 1 })
      if(res.status === 200) {
        this.$message({ message: '修改成功', type: 'success' })
      }
    }
  }
</script>
