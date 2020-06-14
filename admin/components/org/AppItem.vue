<template>
  <div class="app-item">
    <div class="app-item-head" @click="openDetailsDialog">
      <i class="el-icon-delete" v-if="item.type === 'light' && item.own_org_id === currentOrgIdGetter" @click.stop="handleDeleteApp"></i>
      <img class="app-item-image" :src="item.icon" />
      <h2 class="app-item-title">{{item.title}}</h2>
    </div>
    <div class="footer">
      <el-button v-if="item.is_install" type="text" @click="handleIntroApp">进入</el-button>
      <el-button v-if="item.type === 'light' && item.own_org_id === currentOrgIdGetter" type="text" @click="handleEitApp">编辑</el-button>
      <el-button v-if="!item.is_install" type="text" @click="openDetailsDialog">查看详情</el-button>
      <AppToggleBtn type="text" :item="item"></AppToggleBtn>
    </div>
  </div>
</template>
<style lang="scss" scoped>
  @import "../../components/ui/theme/variables";

  .app-item {
    width:235px;
    height:273px;
    background: #FDFDFD;
    border-radius:5px;
    border:1px solid $borderColor;
    display: flex;
    flex-direction: column;
    margin-left: 20px;
    cursor: pointer;
    margin-bottom: 20px;
    position: relative;

    .el-icon-delete {
      position: absolute;
      right: 15px;
      top: 15px;
      color: #f74123;
      font-size: 16px;
    }

    .app-item-head {
      height: 228px;
      align-items: center;
      width: 100%;
      justify-content: center;
      display: flex;
      flex-direction: column;

      .app-item-image {
        width: 132px;
        height: 132px;
      }

      .app-item-title {
        height: 37px;
        font-size: 22px;
        font-family: PingFangSC-Regular,PingFang SC;
        font-weight: 400;
        color: rgba(65,65,65,1);
        line-height: 37px;
        margin-top: 19px;
      }
    }

    .footer {
      border-top: 1px solid $borderColor;
      display: flex;
      .el-button {
        flex: 1;
      }
    }
  }
</style>
<script lang="ts">
  import { Vue, Component, Prop, Emit, namespace } from 'nuxt-property-decorator'
  import AppToggleBtn from './AppToggleBtn.vue'
  import tools from '~/utils'
  import { Confirm } from '~/components/ui'

  const app = namespace('app')

  @Component({
      components: { AppToggleBtn }
  })
  export default class AppItem extends Vue {
    @Prop([Object]) item

    @app.Getter currentOrgIdGetter
    @app.Action removeLightApp

    handleDeleteApp() {
      Confirm.deleteConfirm(this, '成员', () => this.removeLightApp(this.item.id))
          .then(() => this.$emit('onRefreshTable'))
    }

    handleIntroApp() {
      tools.gotoAppIndex(this.item, this.$router)
    }

    handleEitApp() {
      this.$router.push(`/app/light/${this.item.id}`)
    }

    @Emit('onClick')
    openDetailsDialog() {
      return this.item
    }
  }
</script>
