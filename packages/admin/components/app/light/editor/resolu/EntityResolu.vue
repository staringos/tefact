<template>
  <el-form class="entity-resolu" ref="form" :model="form" label-width="80px">
    <el-form-item label="数据源">
      <el-select size="mini" v-model="node.data.dataSourceId" placeholder="请选择">
        <el-option
          v-for="item in options"
          :key="item.id"
          :label="item.name"
          :value="item.id">
        </el-option>
      </el-select>
      <el-button size="mini" icon="el-icon-folder-add" @click="handleOpenDataSource">添加数据源</el-button>
    </el-form-item>
    <el-form-item label="数据表" v-if="node.data.entityId">
      <el-select size="mini" v-model="node.data.entityId" placeholder="请选择">
        <el-option
          v-for="item in options"
          :key="item.value"
          :label="item.label"
          :value="item.value">
        </el-option>
      </el-select>
    </el-form-item>

    <el-dialog
      title="添加数据源"
      :visible.sync="dataSourceDialog"
      width="30%"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      :before-close="handleCloseDataSource">
      <el-form ref="form" :model="form" label-width="80px">
        <el-form-item label="名称">
          <el-input v-model="form.name"></el-input>
        </el-form-item>
        <el-form-item label="类型">
          <el-select v-model="form.type" placeholder="请选择数据源类型">
            <el-option label="Mysql" value="mysql"></el-option>
            <el-option label="Excel" value="excel"></el-option>
            <el-option label="CSV" value="csv"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="数据库地址" v-if="form.type === 'mysql'">
          <el-input v-model="form.address"></el-input>
        </el-form-item>
        <el-form-item label="端口" v-if="form.type === 'mysql'">
          <el-input-number v-model="form.port"></el-input-number>
        </el-form-item>
        <el-form-item label="用户名" v-if="form.type === 'mysql'">
          <el-input v-model="form.username"></el-input>
        </el-form-item>
        <el-form-item label="密码" v-if="form.type === 'mysql'">
          <el-input v-model="form.password"></el-input>
        </el-form-item>
        <el-form-item label="数据库名" v-if="form.type === 'mysql'">
          <el-input v-model="form.dbName"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleAddDataSource">立即创建</el-button>
          <el-button>取消</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>
  </el-form>
</template>
<style lang="scss" scoped>
  .entity-resolu {
    padding: 10px 0;

    /deep/ .el-row {
      padding-bottom: 10px;
    }

    /deep/ .el-form-item {
      margin-bottom: 5px;
    }
  }
</style>
<script lang="ts">
  import { Vue, Component, namespace } from "nuxt-property-decorator";
  import BaseResolu from '~/components/app/light/editor/resolu/BaseResolu.vue'
  import ResoluMixin from '~/components/app/light/editor/resolu/ResoluMixin'
  import ResoluBase from '~/components/app/light/editor/resolu/ResoluClass'
  import * as utils from '~/utils'

  const entities = namespace('entities')
  const editor = namespace('editor')

  @Component({
    components: { BaseResolu },
    mixins: [ ResoluMixin ]
  })
  export default class EntityResolu extends ResoluBase {
    options = []
    form = {}
    dataSourceDialog = false

    @entities.Action getDataSource
    @entities.Action addDataSource
    @editor.Getter currentPage

    async handleOpenDataSource() {
      this.dataSourceDialog = true
    }

    async handleCloseDataSource() {
      this.dataSourceDialog = false
      this.form = {}
    }

    async handleAddDataSource() {
      const data = this.form as any
      data.application_id = this.currentPage.application_id
      data.connect_url = utils.generateMysqlConnectUrl(data)

      delete data.address
      delete data.port
      delete data.dbName

      console.log('[handleAddDataSource] data:', data)

      const res = await this.addDataSource(data)

      if (res.status === 200) {
        this.handleCloseDataSource()
        return this.init()
      }

      this.$message({ message: '操作失败', type: 'error' })

    }

    async init() {
      const res = await this.getDataSource(this.currentPage.application_id)
      this.options = res.data.data
    }

    async mounted() {
      this.init()
    }
  }
</script>
