<template>
  <BaseResolu :title="title" v-bind="$attrs">
    <el-button size="small" type="primary" @click="handleStartEdit()">新增</el-button>
    <FormEdit
      :node="node"
      :nodeType="nodeType"
      :editData="editData"
      :rows="rows"
      @confirm="handleEdit"
      @cancel="handleCancel"
    />
    <div class="list-wrapper">
      <el-table
        class="list-table"
        :data="items"
        size="mini"
        style="width: 100%" v-if="tmpNode">
        <el-table-column type="expand">
          <template slot-scope="props">
            <el-button size="small" type="default" @click="handleStartEdit(props)">修改</el-button>
            <el-button size="small" type="danger" @click="handleDelete(props)">删除</el-button>
          </template>
        </el-table-column>
        <el-table-column
          v-for="(column, i) in columns"
          :prop="column.prop"
          :key="i"
          :label="column.label">
        </el-table-column>
      </el-table>
    </div>
  </BaseResolu>
</template>
<style lang="scss" scoped>
.list-table {
  overflow-x: auto;
}

.modify-form {
  background-color: $gray-02;
  padding: 10px 5px;
}
</style>
<script>
import { Component, Prop } from "nuxt-property-decorator";
import BaseResolu from '~/components/app/light/editor/resolu/BaseResolu.vue'
import ResoluMixin from '~/components/app/light/editor/resolu/ResoluMixin'
import ResoluBase from '~/components/app/light/editor/resolu/ResoluClass'
import Rows from '~/components/app/light/editor/resolu/rows'

import get from 'lodash/get'
import set from 'lodash/set'
import isNumber from 'lodash/isNumber'
import FormEdit from "~/components/app/light/editor/resolu/components/FormEdit";

@Component({
  components: {FormEdit, BaseResolu, ...Rows },
  mixins: [ ResoluMixin ]
})
export default class ListResolu extends ResoluBase {
  @Prop([Array]) rows
  @Prop([String]) title
  @Prop([String]) path

  editData = null

  get items() {
    return get(this.tmpNode, this.path)
  }

  get columns() {
    const columns = []

    this.rows.forEach(cur => {
      columns.push({
        label: cur.params.title,
        prop: cur.params.path,
      })
    })
    return columns
  }

  handleStartEdit(props) {
    if (!this.editData) {
      if (!props) {
        this.editData = {}
      } else {
        this.editData = { ...props.row, i: props.$index }
      }
    }
  }

  handleDelete(props) {
    const list = get(this.tmpNode, this.path)
    const after = list.filter((cur, i) => i !== props.$index)
    set(this.tmpNode, this.path, after)
    this.handleSave()
  }

  handleEdit(data) {
    if (isNumber(data.i)) {
      set(this.tmpNode, this.path + `[${data.i}]`, data)
    } else {
      get(this.tmpNode, this.path).push(data)
    }

    this.handleSave()
    this.handleCancel()
  }

  handleCancel() {
    this.editData = null
  }
}
</script>
