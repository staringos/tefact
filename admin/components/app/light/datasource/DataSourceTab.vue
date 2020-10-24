<template>
  <ArrPanel
    style="margin: 0; height: 200px; flex: none;"
    title="数据源"
    headerButton="el-icon-plus"
    @on-header-button-click="() => handleToggle()"
    border
    header
  >
    <el-table
      :data="dataSourceGetter"
      style="width: 100%"
      :show-header="false"
    >
      <el-table-column
        prop="name"
        label="名"
        width="180">
      </el-table-column>
      <el-table-column
        prop="status"
        label="状态"
        width="180">
      </el-table-column>
      <el-table-column
        prop="operation"
        label="操作">
        <template>
          <el-button icon="el-icon-edit" type="text"></el-button>
          <el-button icon="el-icon-delete" type="text"></el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog title="数据源编辑" :visible.sync="showDialog">
      <el-form :model="form" ref="form" label-width="90px" :rules="rules">
        <el-form-item label="名称">
          <el-input v-model="form.name" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="类型">
          <el-select v-model="form.type" placeholder="请选择数据源类型">
            <el-option label="Mysql" value="mysql"></el-option>
          </el-select>
        </el-form-item>
        <hr />
        <el-form-item label="服务器IP">
          <el-input v-model="form.host" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="端口号">
          <el-input v-model="form.port" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="用户名">
          <el-input v-model="form.username" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="密码">
          <el-input v-model="form.password" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="默认数据库">
          <el-input v-model="form.default_db" autocomplete="off"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="handleCancel">取 消</el-button>
        <el-button @click="handleTest">测试链接</el-button>
        <el-button type="primary" @click="handleSubmit">确 定</el-button>
      </div>
    </el-dialog>
  </ArrPanel>
</template>
<style lang="scss">
  /deep/ .data-source-tab {
    margin: 0;
    height: 100px;
  }
</style>
<script lang="ts">
import { Vue, Component, namespace, Watch } from 'nuxt-property-decorator'
import { DataSource, getDefaultDataSource } from "~/utils/entities/DataSource"

  const app = namespace("app")
  const dataSource = namespace("dataSource")

  @Component
  export default class DataSourceTab extends Vue {
    @app.Getter currentOrgIdGetter
    @dataSource.Getter dataSourceGetter
    @dataSource.Action getDataSourceList
    @dataSource.Action addDataSource
    @dataSource.Action modifyDataSource

    showDialog = false
    form: DataSource = getDefaultDataSource()
    rules: Object = {
      name: [
        { required: true, message: '请输入数据源名称', trigger: 'blur' },
        { min: 3, max: 6, message: '长度在 2 到 6 个字符', trigger: 'blur' }
      ],
      type: [
        { required: true, message: '请选择数据源类型', trigger: 'blur' },
      ],
      host: [
        { required: true, message: '请输入数据源地址', trigger: 'blur' },
      ],
      port: [
        { required: true, message: '请输入数据源端口号', trigger: 'blur' },
      ]
    }

    handleToggle(e?: DataSource) {
      this.showDialog = !this.showDialog
      if (!e) {
        this.form = getDefaultDataSource()
        return;
      }

      this.form = { ...e }
    }

    handleCancel() {
      this.showDialog = false
      this.form = getDefaultDataSource()
    }

    handleTest() {

    }

    handleSubmit() {
      const $form = this.$refs['form'] as any

      $form.validate(async (valid) => {
        if (!valid) return

        this.form.org_id = this.currentOrgIdGetter

        try {
          if (this.form.id) {
            await this.modifyDataSource(this.form.id, this.form)
          } else {
            await this.addDataSource(this.form)
          }
          (this as any).$message({ message: '操作成功', type: 'success' })
          this.handleToggle()
        } catch(e) {
          (this as any).$message({ message: '操作失败: '+ e.message, type: 'error' })
        }
      })

    }

    @Watch("currentOrgIdGetter")
    onOrgIdChange() {
      this.refresh();
    }

    refresh() {
      if (!this.currentOrgIdGetter) return;
      this.getDataSourceList(this.currentOrgIdGetter);
    }

    mounted() {
      this.refresh();
    }
  }
</script>
