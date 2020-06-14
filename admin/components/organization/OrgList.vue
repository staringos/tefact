<template>
  <div class="org-list">
    <ul>
      <li class="item" v-for="(item, index) in allOrgs" :key="index" :command="item.id" @click="() => handleOrgSelect(item.id)">
        <el-avatar :src="item.head_url"></el-avatar>
        <span class="name">{{ item.name }}</span>
        <i class="active el-icon-check" v-if="item.id === currentOrg.id"></i>
      </li>
    </ul>
    <div class="footer">
      <el-button class="add-btn" type="primary" size="small" @click="handleOpenCreateOrg" round>新建组织</el-button>
    </div>
  </div>
</template>
<script lang="ts">
  import { Vue, Component, namespace } from 'nuxt-property-decorator'
  import { DIALOG_NAME } from '~/store/system'

  const app = namespace('app')
  const org = namespace('org')
  const system = namespace('system')

  @Component
  export default class OrgList extends Vue {

    @app.Getter allOrgs
    @app.Getter currentOrg
    @org.Action createOrg
    @app.Action getAllOrgs
    @app.Action onOrgChanged
    @system.Action setDialogVisible

    public async handleOrgSelect(id) {
      const loading = this.$loading({
          lock: true,
          text: 'Loading',
          spinner: 'el-icon-loading',
          background: 'rgba(0, 0, 0, 0.7)'
      })
      await this.onOrgChanged(id)
      loading.close()
    }

    handleOpenCreateOrg() {
      this.setDialogVisible({ key: DIALOG_NAME.CREATE_ORG, visible: true })
    }
  }
</script>
<style lang="scss">
  @import "../../assets/styles/variables";

  .org-list {
    ul {
      .item {
        display: flex;
        line-height: 44px;
        padding: 5px 10px;
        cursor: pointer;
        position: relative;

        &:hover {
          background: $hoverBackground;
        }

        .name {
          margin-left: 10px;
        }

        .active {
          float: right;
          color: #FFF;
          text-align: right;
          background: #d82a2a;
          width: 20px;
          height: 20px;
          border-radius: 50%;
          font-weight: 900;
          display: flex;
          position: absolute;
          right: 10px;
          top: 15px;
          justify-content: center;
          align-items: center;
        }
      }
    }

    .footer {
      border-top: 1px sold $borderColor;
      padding: 10px;
      display: flex;
      justify-content: center;

      .add-btn {
        width: 80%;
      }
    }
  }
</style>
