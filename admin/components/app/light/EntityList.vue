<template>
  <div>
    <ArrTitle bordered>实体列表
      <el-button size="small" icon="el-icon-plus" circle @click="handleEdit()" />
    </ArrTitle>
    <el-table
      :data="entities"
      style="width: 100%">
      <el-table-column type="expand">
        <template slot-scope="props">
          <EntityFieldList :entities="entities" :fields="props.row.fields" :entityId="props.row.id" :globalComponents="globalComponents" @onFieldsChange="(fields) => handleEntityFieldChange(props.row, fields)" />
        </template>
      </el-table-column>
      <el-table-column
        prop="key"
        label="实体KEY"
        width="180">
      </el-table-column>
      <el-table-column
        prop="data_type"
        label="数据类型"
        width="180">
      </el-table-column>
      <el-table-column
        prop="has_connect_org"
        label="联系组织"
        width="180">
      </el-table-column>
      <el-table-column
        prop="sql"
        label="查询语句">
      </el-table-column>
      <el-table-column
        prop="table_name"
        label="数据表名">
      </el-table-column>
      <el-table-column
        prop="options"
        label="操作">
        <template slot-scope="scope">
          <el-button type="default" size="small" round @click="handleEdit(scope.row)">编辑</el-button>
          <el-button type="danger" size="small" round @click="handleDelete(scope.row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog
      title="实体编辑"
      :visible.sync="dialogVisible"
      :model="form"
      :before-close="handleCancel"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      width="50%">
      <el-form label-width="200px" :model="form">
        <el-form-item label="KEY">
          <el-input v-model="form.key"></el-input>
        </el-form-item>
        <el-form-item label="数据表名">
          <el-input v-model="form.table_name"></el-input>
        </el-form-item>
        <el-form-item label="查询语句">
          <el-input v-model="form.sql"></el-input>
        </el-form-item>
        <el-form-item label="类型">
          <el-select v-model="form.type" placeholder="请选择">
            <el-option
              v-for="item in EntityDataType"
              :key="item.key"
              :label="item.value"
              :value="item.key">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="是否与组织系统链接">
          <el-radio v-model="form.has_connect_org" :label="true">显示</el-radio>
          <el-radio v-model="form.has_connect_org" :label="false">隐藏</el-radio>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer" v-if="!isEdit">
        <el-button @click="handleCancel">取 消</el-button>
        <el-button type="primary" @click="handleSave()">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>
<style lang="scss">

</style>
<script lang="ts">
  import { Vue, Component, Prop } from 'nuxt-property-decorator'
  import EntityFieldList from './EntityFieldList.vue';
  import { Constants } from '~/services/common/index.ts'

  @Component({
    components: { EntityFieldList }
  })
  export default class EntitiesList extends Vue {
    @Prop() entities
    @Prop() globalComponents
    @Prop() onChange
    form = { ...Constants.entities.DefaultEntity }
    EntityDataType = Constants.entities.EntityDataType
    dialogVisible = false
    isEdit = false

    PageSectionType = [ ...Constants.entities.PageSectionType ]

    handleEntityFieldChange(entity, fields) {
      Vue.set(entity,'fields', fields)
    }

    handleSave() {
      this.entities.push(this.form)
      this.handleCancel()
    }

    handleEdit(data) {
      if (data) {
        this.form = data
        this.isEdit = true
      }
      this.dialogVisible = true
    }

    handleDelete(data) {
      let current = -1
      this.entities.map((section, i) => {
        if (section === data) {
            current = i
        }
      })
      if (current !== -1) {
        this.entities.splice(current, 1)
      }
    }
    handleCancel() {
      this.dialogVisible = false
      this.isEdit = false
      this.form = { ...Constants.entities.DefaultEntity }
    }
  }
</script>
