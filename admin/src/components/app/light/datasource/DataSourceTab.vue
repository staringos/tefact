<template>
  <ArrPanel
    style="margin: 0; height: 200px; flex: none;"
    title="数据源"
    headerButton="el-icon-plus"
    @on-header-button-click="() => handleToggle()"
    border
    header
    no-padding
  >
    <el-table
      ref="table"
      :data="dataSourceGetter"
      style="width: 100%; max-width: 100%; overflow-y: auto;"
      size="mini"
      :show-header="false"
      :show-overflow-tooltip="true"
      highlight-current-row
      :current-row-key="value"
      @current-change="handleCurrentChange"
    >
      <el-table-column
        prop="name"
        width="130"
        label="名">
      </el-table-column>
      <el-table-column
        prop="status"
        width="35"
        label="状态">
        <template slot-scope="scope">
          <i v-if="scope.row.status === 'connected'" class="el-icon-check" style="color: green;"></i>
          <i v-if="scope.row.status === 'error'" class="el-icon-close" style="color: red;"></i>
          <i v-if="!scope.row.status || scope.row.status === 'default' " class="el-icon-info" style="color: green;"></i>
        </template>
      </el-table-column>
      <el-table-column
        prop="operation"
        label="操作">
        <template slot-scope="scope">
          <el-button icon="el-icon-edit" @click="handleToggle(scope.row)" type="text"></el-button>
          <el-button icon="el-icon-delete" @click="handleDelete(scope.row)" type="text"></el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog title="数据源编辑" :visible.sync="showDialog">
      <el-form :model="form" ref="form" label-width="100px" :rules="rules">
        <el-form-item label="名称" prop="name">
          <el-input v-model="form.name" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="类型" prop="type">
          <el-select v-model="form.type" placeholder="请选择数据源类型">
            <el-option label="Mysql" value="mysql"></el-option>
          </el-select>
        </el-form-item>
        <hr />
        <el-form-item label="服务器IP" prop="host">
          <el-input v-model="form.host" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="端口号" prop="port">
          <el-input v-model="form.port" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="用户名" prop="username">
          <el-input v-model="form.username" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input v-model="form.password" autocomplete="off" type="password"></el-input>
        </el-form-item>
        <el-form-item label="默认数据库" prop="default_db">
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
::v-deep .data-source-tab {
    margin: 0;
    height: 100px;
  }
</style>
<script lang="ts">
  import identity from 'lodash/identity'
  import pickBy from 'lodash/pickBy'
  import { Vue, Component, Prop, namespace, Watch } from 'nuxt-property-decorator'
  import { DataSource, getDefaultDataSource } from "~/utils/entities/DataSource"
  import { Confirm } from '~/components/ui'

  const app = namespace("app")
  const dataSource = namespace("dataSource")
  const PLACEHOLDER_PASSWORD = "$$PLACEHOLDER_PASSWORD$$"

  @Component
  export default class DataSourceTab extends Vue {
    @Prop() value

    @app.Getter currentOrgIdGetter
    @dataSource.Getter dataSourceGetter
    @dataSource.Action getDataSourceList
    @dataSource.Action addDataSource
    @dataSource.Action modifyDataSource
    @dataSource.Action deleteDataSource
    @dataSource.Action testConnect

    showDialog = false
    form: DataSource = getDefaultDataSource()
    rules: Object = {
      name: [
        { required: true, message: '请输入数据源名称', trigger: 'blur' },
        { min: 3, max: 12, message: '长度在 2 到 12 个字符', trigger: 'blur' }
      ],
      type: [
        { required: true, message: '请选择数据源类型', trigger: 'blur' },
      ],
      host: [
        { required: true, message: '请输入数据源地址', trigger: 'blur' },
      ],
      port: [
        { required: true, message: '请输入数据源端口号', trigger: 'blur' },
      ],
      "default_db": [
        { required: true, message: '请输入默认数据库名', trigger: 'blur' },
      ]
    }

    handleCurrentChange(e) {
      this.$emit("input", e.id)
    }

    handleDelete(row) {
      Confirm.deleteConfirm(this, '数据源', () => this.deleteDataSource(row.id))
        .then(() => this.refresh())
    }

    handleToggle(e?: DataSource) {
      this.showDialog = !this.showDialog
      if (!e) {
        this.form = getDefaultDataSource()
        return;
      }

      this.form = { ...e }
      if (!this.form.password) {
        this.form.password = PLACEHOLDER_PASSWORD
      }
    }

    handleCancel() {
      this.showDialog = false
      this.form = getDefaultDataSource()
    }

    async handleTest() {
      const that = (this as any)

      try {
        await this.testConnect(this.form)
        that.$message({ message: '连接成功', type: 'success' })
      } catch(e) {
        that.$message({ message: e.data.message, type: 'error' })
      }
    }

    handleSubmit() {
      const $form = this.$refs['form'] as any

      $form.validate(async (valid) => {
        if (!valid) return

        this.form.org_id = this.currentOrgIdGetter
        const form = pickBy(this.form, identity)

        try {
          if (form.id) {
            if (form.password === PLACEHOLDER_PASSWORD) delete form.password
            await this.modifyDataSource({ id: form.id, data: form })
          } else {
            await this.addDataSource(form)
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

    async refresh() {
      if (!this.currentOrgIdGetter) return;
      const res = await this.getDataSourceList(this.currentOrgIdGetter);
      const first = res?.[0];
      if (first) {
        (this.$refs.table as any).setCurrentRow(first);
        this.handleCurrentChange(first)
      }
    }

    mounted() {
      this.refresh();
    }
  }
</script>
