<template>
  <div>
    <ArrTitle bordered>字段列表
      <el-button size="small" icon="el-icon-plus" circle @click="handleEdit()" />
    </ArrTitle>
    <el-table :data="fields" style="width: 100%">
      <el-table-column prop="key" label="KEY"></el-table-column>
      <el-table-column prop="name" label="字段名"></el-table-column>
      <el-table-column prop="type" label="类型"></el-table-column>
      <el-table-column prop="data_type" label="数据类型"></el-table-column>
      <el-table-column prop="display_type" label="显示类型"></el-table-column>
      <el-table-column prop="exists" label="显示模块"></el-table-column>
      <el-table-column prop="options" label="操作">
        <template slot-scope="scope">
          <el-button-group>
            <el-button type="default" size="small" round @click="switchSort(scope.$index, 1)" icon="el-icon-top"></el-button>
            <el-button type="default" size="small" round @click="switchSort(scope.$index, 0)" icon="el-icon-bottom"></el-button>
          </el-button-group>

          <el-button-group>
            <el-button type="default" size="small" round @click="handleEdit(scope.row)">编辑</el-button>
            <el-button type="danger" size="small" round @click="handleDelete(scope.row)">删除</el-button>
          </el-button-group>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog
      title="实体字段编辑"
      :visible.sync="dialogVisible"
      :model="form"
      :before-close="handleCancel"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      width="50%">
      <el-form label-width="200px" :model="form" :rules="rules">
        <el-tabs v-model="activeForm">
          <el-tab-pane label="基础信息" name="first">
            <el-form-item label="是否为主键" required>
              <el-radio v-model="form.is_primary" :label="true">是</el-radio>
              <el-radio v-model="form.is_primary" :label="false">否</el-radio>
            </el-form-item>
            <el-form-item label="KEY" required>
              <el-input v-model="form.key"></el-input>
            </el-form-item>
            <el-form-item label="表名">
              <el-input v-model="form.table_name"></el-input>
            </el-form-item>
            <el-form-item label="实体字段名" required>
              <el-input v-model="form.name"></el-input>
            </el-form-item>
<!--            <el-form-item label="排序">-->
<!--              <el-input-number v-model="form.sort" :min="0" :max="100"></el-input-number>-->
<!--              <el-button size="tiny" type="default" @click="handleRemoveSort">默认</el-button>-->
<!--            </el-form-item>-->
            <el-form-item label="显示">
              <el-select v-model="form.exists" multiple placeholder="请选择">
                <el-option v-for="item in EntityFieldExists" :key="item.key" :label="item.value" :value="item.key">
                </el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="类型">
              <el-select v-model="form.type" placeholder="请选择">
                <el-option v-for="item in EntityFieldType" :key="item.key" :label="item.value" :value="item.key">
                </el-option>
              </el-select>
            </el-form-item>

            <el-form-item label="数据类型">
              <el-select v-model="form.data_type" placeholder="请选择">
                <el-option v-for="item in EntityFieldDataType" :key="item.key" :label="item.value" :value="item.key">
                </el-option>
              </el-select>

              <el-select v-model="form.form_component" placeholder="请选择表单组件"  v-if="form.data_type === 'global-component'">
                <el-option v-for="item in globalComponents" :key="item.name" :label="item.name" :value="item.name">
                </el-option>
              </el-select>
            </el-form-item>

            <div class="form-panel" v-if="form.data_type === 'foreign-key'">
              <ArrTitle bordered>外键</ArrTitle>
              <el-form-item label="展示类型" required>
                <el-select v-model="form.foreign_type" placeholder="请选择展示类型">
                  <el-option v-for="item in EntityForeignType" :key="item.key" :label="item.value" :value="item.key">
                  </el-option>
                </el-select>
              </el-form-item>
              <el-form-item label="数据源SQL">
                <el-input v-model="form.data_source_sql"></el-input>
              </el-form-item>
              <ArrTitle bordered v-if="form.foreign_type === 'many-to-many'">多对多中间表</ArrTitle>
              <el-form-item label="表名" v-if="form.foreign_type === 'many-to-many'">
                <el-input v-model="form.foreign_table_name"></el-input>
              </el-form-item>
              <el-form-item label="本表外键名" v-if="form.foreign_type === 'many-to-many'">
                <el-input v-model="form.foreign_our_key"></el-input>
              </el-form-item>
              <el-form-item label="它表外键名" v-if="form.foreign_type === 'many-to-many'">
                <el-input v-model="form.foreign_their_key"></el-input>
              </el-form-item>
            </div>

            <el-form-item label="展示类型">
              <el-select v-model="form.display_type" placeholder="请选择展示类型">
                <el-option v-for="item in EntityFieldDisplayType" :key="item.key" :label="item.value" :value="item.key">
                </el-option>
              </el-select>

              <el-select v-model="form.display_component" placeholder="请选择展示组件" v-if="form.display_type === 'global-component'">
                <el-option v-for="item in globalComponents" :key="item.name" :label="item.name" :value="item.name">
                </el-option>
              </el-select>
            </el-form-item>

            <el-form-item label="按钮组" v-if="form.type === 'buttons'">
              <el-tag v-for="(button, i) in form.buttons" :key="i" closable type="info" @close="handleRemoveButton(button)">
                type: {{button.type}} link: {{button.link}}
              </el-tag>

              <ButtonForm has-name :entities="entities" v-model="tmpButton"></ButtonForm>
              <el-button type="primary" size="small" @click="handleAddButton">添加</el-button>
            </el-form-item>
            <el-form-item label="字典数据" v-if="form.data_type === 'dict'" required>
              <el-tag v-for="(dict, i) in form.dict_list" :key="i" closable type="info" @close="handleDeleteDict(dict)">
                Key: {{dict.key}} Value: {{dict.value}}
              </el-tag>
              <el-row style="background: #e2e3e6; padding: 20px;">
                <el-col :span="8">
                  <el-input v-model="tmpDict.key" placeholder="KEY"></el-input>
                </el-col>
                <el-col :span="8">
                  <el-input v-model="tmpDict.value" placeholder="VALUE"></el-input>
                </el-col>
                <el-col :span="4">
                  <el-button type="primary" size="small" @click="handleAddDict">添加</el-button>
                </el-col>
              </el-row>
            </el-form-item>
            <el-form-item label="SQL" v-if="form.type === 'sql'" required>
              <el-input v-model="form.sql"></el-input>
            </el-form-item>
            <el-form-item label="嵌入URL" v-if="form.display_type === 'custom'">
              <el-input v-model="form.iframe_url"></el-input>
            </el-form-item>
            <el-form-item label="跳转连接">
              <el-radio v-model="form.has_link" :label="true">显示</el-radio>
              <el-radio v-model="form.has_link" :label="false">隐藏</el-radio>
              <el-select v-if="form.has_link" v-model="linkType" placeholder="请选择连接类型">
                <el-option v-for="item in EntityFieldLinkType" :key="item.key" :label="item.value" :value="item.key"></el-option>
              </el-select>
              <el-input v-if="linkType === 'link' && form.has_link" v-model="form.link_address" placeholder="请输入跳转链接"></el-input>
              <ButtonForm v-if="linkType === 'button' && form.has_link" :entities="entities" v-model="form.link_button"></ButtonForm>
            </el-form-item>
          </el-tab-pane>
          <el-tab-pane label="附加配置" name="second">
            <el-form-item label="可排序">
              <el-radio v-model="form.has_sort" :label="true">显示</el-radio>
              <el-radio v-model="form.has_sort" :label="false">隐藏</el-radio>
            </el-form-item>
            <el-form-item label="可搜索">
              <el-radio v-model="form.has_search" :label="true">显示</el-radio>
              <el-radio v-model="form.has_search" :label="false">隐藏</el-radio>
            </el-form-item>
            <ArrTitle bordered>编辑页</ArrTitle>
            <el-form-item label="默认值" v-if="['string', 'number', 'boolean'].indexOf(form.data_type) !== -1">
              <el-input v-model="form.default_value" v-if="form.data_type === 'string'"></el-input>
              <el-input-number v-model="form.default_value" v-if="form.data_type === 'number'"></el-input-number>

              <el-radio v-model="form.default_value" v-if="form.data_type === 'boolean'" :label="true">是</el-radio>
              <el-radio v-model="form.default_value" v-if="form.data_type === 'boolean'" :label="false">否</el-radio>
            </el-form-item>
            <el-form-item label="字段描述">
              <el-input v-model="form.description"></el-input>
            </el-form-item>
            <ArrTitle bordered>表单验证</ArrTitle>
            <el-form-item label="必填" required>
              <el-switch v-model="form.verify_require" />
            </el-form-item>
            <el-form-item label="唯一">
              <el-switch v-model="form.verify_only" />
            </el-form-item>
            <el-form-item :label="form.data_type === 'number' ? '最大值' : '最大长度'" v-if="['number', 'string'].indexOf(form.data_type) !== -1">
              <el-input-number v-model="form.verify_max" :min="0" :step="1"></el-input-number>
            </el-form-item>
            <el-form-item :label="form.data_type === 'number' ? '最小值' : '最小长度'" v-if="['number', 'string'].indexOf(form.data_type) !== -1">
              <el-input-number v-model="form.verify_min" :min="0" :step="1"></el-input-number>
            </el-form-item>
            <el-form-item label="验证正则">
              <el-input v-model="form.verify_pattern"></el-input>
            </el-form-item>
          </el-tab-pane>
        </el-tabs>
      </el-form>
      <span slot="footer" class="dialog-footer" v-if="!isEdit">
        <el-button @click="handleCancel">取 消</el-button>
        <el-button type="primary" @click="handleSave()">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>
<style lang="scss" scoped>
  .form-panel {
    border-top: 1px solid #DCDFE6;
    border-bottom: 1px solid #DCDFE6;
  }
</style>
<script lang="ts">
  import { Vue, Component, Prop, Emit, Watch } from 'nuxt-property-decorator'
  import { Constants } from '@arrplat/common'
  import { reorder } from '../utils'
  import ButtonForm from './ButtonForm.vue'

  @Component({
    components: { ButtonForm }
  })
  export default class EntityFieldList extends Vue {
    @Prop() globalComponents
    @Prop() fields
    @Prop() entityFieldChange
    @Prop() entityId
    @Prop() entities

    activeForm = 'first'
    rules = {}
    linkType = 'link'

    form = JSON.parse(JSON.stringify(Constants.entities.DefaultEntityField))
    EntityFieldType = Constants.entities.EntityFieldType
    EntityFieldDataType = Constants.entities.EntityFieldDataType
    EntityFieldDisplayType = Constants.entities.EntityFieldDisplayType
    EntityFieldExists = Constants.entities.EntityFieldExists
    EntityForeignType = Constants.entities.EntityForeignType
    EntityFieldLinkType = Constants.entities.EntityFieldLinkType
    ButtonType = Constants.entities.ButtonType

    dialogVisible = false
    isEdit = false
    tmpDict = { key: '', value: '' }
    tmpButton = { link: '', type: '', name: '' }
    PageSectionType = [ ...Constants.entities.PageSectionType ]

    switchSort(i, flag) {
      reorder(this.fields, i, flag)
    }

    handleAddButton() {
      if (!this.tmpButton.type) return
      if (this.form.buttons) this.form.buttons.push({ ...this.tmpButton })
      else this.form.buttons = [{ ...this.tmpButton }]

      this.tmpButton = { link: '', type: '', name: '' }
    }

    handleRemoveButton(button) {
      this.form.buttons.splice(this.form.buttons.indexOf(button), 1);
    }

    handleRemoveSort() {
      delete this.form.sort
    }

    handleDeleteDict(dict) {
      this.form.dict_list.splice(this.form.dict_list.indexOf(dict), 1);
    }

    handleAddDict() {
      this.form.dict_list.push(this.tmpDict)
      this.tmpDict = { key: '', value: '' }
    }

    handleSave() {
      this.fields.push(this.form)
      this.handleCancel()
    }

    handleEdit(data) {
      if (data) {
        this.form = data
        this.isEdit = true
      }

      if (this.form.link_button) this.linkType = this.form.link_button.type ? 'button' : 'link'
      this.dialogVisible = true
    }

    handleDelete(data) {
      let current = -1
      this.fields.map((section, i) => {
        if (section === data) {
          current = i
        }
      })
      if (current !== -1) {
        this.fields.splice(current, 1)
      }
    }
    handleCancel() {
      this.dialogVisible = false
      this.isEdit = false
      this.form = JSON.parse(JSON.stringify(Constants.entities.DefaultEntityField))
    }
  }
</script>
