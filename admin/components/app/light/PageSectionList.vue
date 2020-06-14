<template>
  <div>
    <ArrTitle bordered>Section列表
      <el-button size="small" icon="el-icon-plus" circle @click="handleEdit()" />
    </ArrTitle>
    <el-table
      :data="sections"
      style="width: 100%">
      <el-table-column
        prop="entity_key"
        label="实体KEY"
        width="180">
      </el-table-column>
      <el-table-column
        prop="has_add_btn"
        label="显示添加按钮"
        width="180">
      </el-table-column>
      <el-table-column
        prop="title"
        label="标题">
      </el-table-column>
      <el-table-column
        prop="type"
        label="类型">
      </el-table-column>
      <el-table-column
        prop="sort"
        label="排序">
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
      title="页面Section编辑"
      :visible.sync="dialogVisible"
      :model="form"
      :before-close="handleCancel"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      width="30%">
      <el-form label-width="80px" :model="form">
        <el-form-item label="标题">
          <el-input v-model="form.title"></el-input>
        </el-form-item>
        <el-form-item label="实体KEY">
<!--          <el-input v-model="form.entity_key"></el-input>-->
          <el-select v-model="form.entity_key" placeholder="请选择">
            <el-option
              v-for="item in entities"
              :key="item.key"
              :label="item.key"
              :value="item.key">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="实体参数">
          <el-input v-model="form.entity_params"></el-input>
        </el-form-item>
        <el-form-item label="类型">
          <el-select v-model="form.type" placeholder="请选择">
            <el-option
              v-for="item in PageSectionType"
              :key="item.key"
              :label="item.value"
              :value="item.key">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="显示增加按钮">
          <el-radio v-model="form.has_add_btn" :label="true">显示</el-radio>
          <el-radio v-model="form.has_add_btn" :label="false">隐藏</el-radio>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer" v-if="!isEdit">
        <el-button @click="dialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="handleSave()">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>
<style lang="scss">

</style>
<script lang="ts">
  import { Vue, Component, Prop } from 'nuxt-property-decorator'
  import { Constants } from '~/services/common'

  @Component
  export default class AppItem extends Vue {
    @Prop() sections
    @Prop() entities
    dialogVisible = false
    isEdit = false
    form = { ...Constants.entities.DefaultPageSection }
    PageSectionType = [ ...Constants.entities.PageSectionType ]

    handleSave() {
      this.sections.push(this.form)
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
      this.sections.map((section, i) => {
        if (section === data) {
          current = i
        }
      })
      if (current !== -1) {
        this.sections.splice(current, 1)
      }
    }
    handleCancel() {
      this.dialogVisible = false
      this.isEdit = false
      this.form = { ...Constants.entities.DefaultPageSection }
    }
  }
</script>
