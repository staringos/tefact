<template>
  <div class="toolbar">
    <el-popover
      popper-class="popover-no-padding"
      placement="bottom-start"
      title="我的组织"
      width="200"
      trigger="click"
      v-if="currentOrg">
      <span class="org-select el-dropdown-link toolbar-item" slot="reference">
        {{currentOrg.name}}<i class="el-icon-arrow-down"></i>
      </span>
      <OrgList />
    </el-popover>
    <el-button class="toolbar-btn toolbar-item" type="text" @click="toOrgManage">
      <i class="el-icon-setting"></i>
    </el-button>
    <el-popover
      popper-class="popover-no-padding last-button"
      placement="bottom-start"
      title="系统消息"
      width="200"
      trigger="click">
      <MessageList @onDataRefresh="handleUnreadNumber"/>
      <el-button class="toolbar-btn toolbar-item" type="text" slot="reference">
        <i class="el-icon-bell"></i>
        <el-badge class="toolbar-btn-badge" :hidden="unreadNumber < 1" :value="unreadNumber"></el-badge>
      </el-button>
    </el-popover>
  </div>
</template>
<script lang="ts">
  import { Component, Vue, namespace } from 'nuxt-property-decorator'
  import MessageList from '../message/MessageList.vue'
  import OrgList from '../organization/OrgList.vue'

  const app = namespace('app')

  @Component({
    components: {
      OrgList,
      MessageList
    }
  })
  export default class HeaderProfile extends Vue {
    unreadNumber: number = 0
    circleUrl: string = ''

    @app.Getter currentOrg
    @app.Action onOrgChanged: any
    @app.Action setOrgDialogFlag: any

    toOrgManage() {
      this.$router.push('/plugins/org')
    }

    handleUnreadNumber(unreadNumber) {
      this.unreadNumber = unreadNumber
    }
  }
</script>
<style lang="scss">
  @import "../../assets/styles/variables";

  .toolbar {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100%;

    .toolbar-item {
      margin-right: 20px;
    }

    .el-button {
      font-size: 18px;
      &:focus {
        outline: 0;
      }
    }

    .last-button {
      margin-right: 10px;
    }

    .header-operation {
      .el-dropdown {
        margin-right: 15px;
        .item {
          margin: 0;
          padding: 0;
        }
      }
    }

    .org-select {
      cursor: pointer;
      &:focus {
        outline: 0;
      }
    }

    .toolbar-btn {
      position: relative;

      .toolbar-btn-badge {
        position: absolute;
        left: 10px;
        display: inline-block;
      }
    }
  }

  .popover-no-padding {
    padding: 0;
    width: auto !important;
    min-width: 200px !important;

    .el-popover__title {
      padding: 20px 10px 0px 10px;
    }
  }
</style>
