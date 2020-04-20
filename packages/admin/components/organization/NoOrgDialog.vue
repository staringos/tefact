<template>
  <DialogX title="创建组织" :DialogKey="DialogKey" ref="dialog" :show-close="false">
    <p class="dialog-content-p">您还未加入任何组织，立即免费创建组织</p>
    <div class="dialog-footer" slot="footer">
      <el-button type="primary" size="small" @click="handleAddOrg">创建组织</el-button>
    </div>
  </DialogX>
</template>
<style lang="scss">
  .dialog-content-p {
    text-align: center;
  }
</style>
<script lang="ts">
  import { Vue, Component, namespace, Watch } from 'nuxt-property-decorator'
  import { DialogX } from '@arrplat/ui'
  import { DIALOG_NAME } from '~/store/system'

  const system = namespace('system')
  const app = namespace('app')

  @Component({
    components: { DialogX }
  })
  export default class NoOrgDialog extends Vue {
    DialogKey: string = DIALOG_NAME.NO_ORG_DIALOG

    @system.Action setDialogVisible
    @app.Action allOrgs

    @Watch('allOrgs')
    onAllOrgsChange() {
      (this.$refs.dialog as any).handleClose()
    }

    handleAddOrg() {
      this.setDialogVisible({ key: DIALOG_NAME.CREATE_ORG, visible: true })
    }
  }
</script>
