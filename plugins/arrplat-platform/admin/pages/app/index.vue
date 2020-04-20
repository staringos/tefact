<template>
  <ArrPanel class="app-option-list" title="应用列表" border>
    <div class="width-full">
      <el-table
        :data="appsGetter"
        :default-sort = "{prop: 'date', order: 'descending'}"
      >
        <el-table-column
          prop="date"
          label="ICON"
          sortable
          width="180">
          <template slot-scope="scope">
            <el-avatar :size="60" :src="scope.row.icon" circle></el-avatar>
          </template>
        </el-table-column>
        <el-table-column
          prop="key"
          label="Key"
          sortable
          width="180">
        </el-table-column>
        <el-table-column
          prop="title"
          label="应用名"
          sortable
          width="180">
        </el-table-column>
        <el-table-column
          prop="description"
          label="描述">
        </el-table-column>
        <el-table-column
          prop="api_route"
          label="接口跟路由">
        </el-table-column>
        <el-table-column
          prop="admin_route"
          label="后台跟路由">
        </el-table-column>
        <el-table-column
          prop="admin_route"
          label="操作">
          <template slot-scope="scope">
            <el-button type="default" size="small" @click="goDetails(scope.row.key)" round>详情</el-button>
            <el-button type="danger" size="small" round>删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
  </ArrPanel>
</template>
<style lang="scss">
  .app-option-list {
    .el-avatar {
      background: none;
    }
  }
</style>
<script lang="ts">
    import { Vue, Component, namespace} from 'nuxt-property-decorator'
    import { Application } from '@arrplat/common'

    const platform = namespace('platform')

    @Component({
      layout: 'plugin',
    })
    export default class AppPage extends Vue {
      @platform.Getter appsGetter
      @platform.Action getPlatformConfig

      public async beforeMount() {
        await this.getPlatformConfig()
      }

      public goDetails(key) {
        this.$router.push(`/plugins/platform/app/${key}`)
      }
    }
</script>
