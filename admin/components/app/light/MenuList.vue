<template>
  <div class="menu-list">
    <ArrTitle bordered>菜单列表
      <el-button size="small" icon="el-icon-plus" circle @click="handleDialogOpen()" />
    </ArrTitle>
    <el-table
      :data="treeMenus"
      style="width: 100%;"
      row-key="id"
      border
      :tree-props="{children: 'children', hasChildren: 'hasChildren'}">
      <el-table-column prop="date" label="子菜单" width="80"></el-table-column>
      <el-table-column prop="name" label="姓名" sortable>
        <template slot-scope="scope">
          <el-avatar :src="scope.row.icon" v-if="scope.row.icon && scope.row.icon.indexOf('http') !== -1" />
          <i :class="scope.row.icon" v-if="scope.row.icon && scope.row.icon.indexOf('http') === -1" />
          <span>{{scope.row.name}}</span>
        </template>
      </el-table-column>
      <el-table-column prop="link" label="链接"></el-table-column>
      <el-table-column prop="page_key" label="页面"></el-table-column>
      <el-table-column prop="type" label="菜单类型"></el-table-column>
      <el-table-column prop="sort" label="操作" width="180">
        <template slot-scope="scope">
          <el-button-group>
            <el-button type="default" size="small" round @click="switchSort(scope.row, 1)" icon="el-icon-top"></el-button>
            <el-button type="default" size="small" round @click="switchSort(scope.row, 0)" icon="el-icon-bottom"></el-button>
          </el-button-group>
          <el-button-group>
            <el-button type="default" size="small" round @click="handleEdit(scope.row)" icon="el-icon-edit"></el-button>
            <el-button type="danger" size="small" round @click="handleDelete(scope.row)" icon="el-icon-delete"></el-button>
          </el-button-group>

          <el-button type="default" size="small" @click="handleDialogOpen(scope.row)" round>添加子菜单</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog
      title="菜单编辑"
      :visible.sync="dialogVisible"
      :before-close="handleCancel"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      width="30%">
      <el-form label-width="80px" :model="form">
        <el-form-item label="菜单名">
          <el-input v-model="form.name"></el-input>
        </el-form-item>
<!--        <el-form-item label="排序">-->
<!--          <el-input v-model="form.sort"></el-input>-->
<!--          <el-button type="danger" size="tiny" @click="handleClearSort">清除</el-button>-->
<!--        </el-form-item>-->
        <el-form-item label="ICON">
          <el-input v-model="form.icon"></el-input>
        </el-form-item>
        <el-form-item label="链接">
          <el-input v-model="form.link"></el-input>
        </el-form-item>
        <el-form-item label="类型">
          <el-select v-model="form.type" placeholder="请选择">
            <el-option
              v-for="item in MenuType"
              :key="item.key"
              :label="item.value"
              :value="item.key">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="关联页面">
          <el-select v-model="form.page_key">
            <el-option
              v-for="(page, i) in pages"
              :key="page.key"
              :label="page.title"
              :value="page.key">
            </el-option>
          </el-select>
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
  .menu-list {
    flex: 1;
  }
</style>
<script lang="ts">
  import { Vue, Component, Prop, namespace } from 'nuxt-property-decorator'
  import { Constants } from '~/services/common'
  import { reorder, loopModify, loopChildren } from '~/utils/light'
  import { cloneDeep } from "lodash-es";

  const app = namespace('app')

  @Component
  export default class MenuList extends Vue {
    @Prop() menus
    @Prop() pages
    @Prop() appId
    @Prop() onChange
    @app.Action addMenu
    @app.Action deleteMenu
    @app.Action modifyMenu

    dialogVisible = false
    form = { ...Constants.entities.DefaultMenu }
    isEdit = false
    parentMenu = null
    MenuType = Constants.entities.MenuType

    public async switchSort(data, flag) {
      await loopModify(this.menus, data, null, 'reorder', flag)
    }

    public async handleDelete(data) {
      const res = await loopModify(this.menus, data)
      this.onChange(res)
    }

    public handleCancel() {
      this.dialogVisible = false
      this.form = { ...Constants.entities.DefaultMenu }
      this.isEdit = false
      this.parentMenu = null
    }

    public handleEdit(data) {
      this.form = cloneDeep(data.menu)
      this.dialogVisible = true
      this.isEdit = true
    }

    public async handleSave() {
      if (!this.isEdit && !this.parentMenu) {
        this.form.application_id = this.appId
        await this.addMenu(this.form)
      } else {
        await this.modifyMenu(this.form.id, this.form)
      }

      this.handleCancel()
    }

    public handleDialogOpen(parent = null) {
      this.dialogVisible = true
      this.parentMenu = parent
    }

    get treeMenus() {
      return loopChildren(this.menus)
    }
  }
</script>
