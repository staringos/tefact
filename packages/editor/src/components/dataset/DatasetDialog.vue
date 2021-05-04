<template>
  <el-dialog
    title="数据项管理"
    :visible.sync="value"
    class="dataset-dialog"
    :before-close="handleClose"
    width="70%"
  >
    <div class="dataset-wrapper">
      <el-tree
        class="dataset-tree"
        :data="datasetTree"
        :props="defaultProps"
        @current-change="handleCurrentChange"
        default-expand-all
      >
        <span
          class="tree-operations"
          slot-scope="{ node, data }"
          @click.stop="handleCurrentChange(node, data)"
        >
          <span class="title">{{ node.label }}</span>
          <span class="btns">
            <el-button
              type="text"
              icon="el-icon-plus"
              circle
              size="mini"
              v-if="node.level === 1"
              @click="() => handleAddDataset(node, data)"
            ></el-button>
            <el-button
                type="text"
                icon="el-icon-delete"
                circle
                size="mini"
                v-if="node.level === 2"
                @click="() => handleDeleteDataset(node, data)"
            ></el-button>
          </span>
        </span>
      </el-tree>
      <div class="dataset-modify">
        <el-form
          v-if="isEditing"
          ref="form"
          :model="form"
          label-width="100px"
        >
          <el-form-item label="名称">
            <el-input v-model="form.name"></el-input>
          </el-form-item>
          <el-form-item label="标识">
            <el-input v-model="form.union" :disabled="isModify"></el-input>
          </el-form-item>
          <el-form-item label="数据项类型">
            <el-select v-model="form.type" placeholder="数据项类型" :disabled="isModify">
              <el-option label="数据源" value="datasource" disabled></el-option>
              <el-option label="自定义" value="custom"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="数据类型">
            <el-select v-model="form.data_type" placeholder="数据项类型" @change="handleDataTypeChange" :disabled="isModify">
              <el-option label="列表" value="array"></el-option>
              <el-option label="对象" value="object"></el-option>
              <el-option label="字符串" value="string"></el-option>
              <el-option label="布尔" value="boolean"></el-option>
              <el-option label="数值" value="number"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="数据">
            <el-input type="textarea" v-model="form.data"></el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleSubmit">立即创建</el-button>
            <el-button>取消</el-button>
          </el-form-item>
        </el-form>
        <p v-else>请在左侧选择或创建数据项</p>
      </div>
    </div>
  </el-dialog>
</template>
<style lang="scss" scoped>
$border: #f5f5f5;
.dataset-dialog {
  .dataset-wrapper {
    display: flex;
    min-height: 300px;

    .dataset-tree {
      width: 200px;
      background-color: $border;

      ::v-deep.tree-operations {
        width: 100%;
        flex: 1;
        display: inline-block;

        .title {
          line-height: 28px;
          width: 100px;
          display: inline-block;
          overflow:hidden; //超出的文本隐藏
          text-overflow:ellipsis; //溢出用省略号显示
          white-space:nowrap; //溢出不换行
        }

        .btns {
          width: 50px;
          float: right;
        }
      }
    }
    .dataset-modify {
      flex: 1;
      border-top: 1px solid $border;
      border-right: 1px solid $border;
      border-bottom: 1px solid $border;
      padding: 20px;
    }
  }
}
</style>
<script lang="ts">
import { Component, Prop } from "vue-property-decorator";
import Previewer from "../common/Previewer.vue";
import SharePageEditor from "../common/SharePageEditor.vue";
import { BaseView, DefaultDataset, IDataSet } from "@tefact/core";
import groupBy from "lodash/groupBy";
import cloneDeep from "lodash/cloneDeep";
import { Confirm } from "@tefact/ui"

const DATA_TYPES = {
  string: "",
  array: [],
  object: {},
  boolean: true,
  number: 0,
}

@Component({
  components: { Previewer, SharePageEditor },
})
export default class DataSetDialog extends BaseView {
  @Prop(Boolean) value;

  defaultProps = {};
  currentDataset = null;
  isEditing = false;
  form = null as null | IDataSet;

  datasetTree = [
    {
      label: "全局数据项",
      children: [
        {
          label: "二级 1-1",
        },
      ],
    },
    {
      label: "页面1 数据项",
      children: [],
    },
    {
      label: "页面2 数据项",
      children: [
        {
          label: "二级 3-1",
          children: [
            {
              label: "三级 3-1-1",
            },
          ],
        },
        {
          label: "二级 3-2",
          children: [
            {
              label: "三级 3-2-1",
            },
          ],
        },
      ],
    },
  ];

  get isModify() {
    return this.form && !!this.form.id;
  }

  handleDataTypeChange(e) {
    if (!this.form) return;
    this.form.data = JSON.stringify(DATA_TYPES[e]) as any;
  }

  handleCurrentChange(node, data) {
    if (node.level === 1) {
      this.isEditing = false;
    }

    this.isEditing = true;
    this.form = data.data;
  }

  async handleDeleteDataset(node, data) {
    const { onDeleteDataSet, onGetDataSet } = this.setting;

    Confirm.deleteConfirm(this, '数据项', () => onDeleteDataSet && onDeleteDataSet(data.data.id))
      .then(async () => {
        if (!onGetDataSet) return;
        const datasets = await onGetDataSet();
        if (datasets) this.refresh(datasets);

        this.isEditing = false;
        this.form = null;
      })
  }

  handleAddDataset(node: any, data: any) {
    this.isEditing = true;
    const form = cloneDeep(DefaultDataset) as IDataSet;
    form.application_id = this.currentTarget.application_id as any;

    if (data.name === "全局") {
      form.bind_type = "app";
      form.target_id = "";
    } else {
      form.bind_type = 'target';
      form.target_id = data.data.id;
    }
    this.form = form;
  }

  handleClose() {
    this.$emit("input", false);
  }

  async refresh(datasets: Array<IDataSet>) {
    const grouped = groupBy(datasets, "target_id")
    const global = groupBy(datasets, "bind_type")['app']

    let datasetTree = [{
      label: "全局",
      isLeaf: false,
      children: global ? global.map(cur => ({
        label: cur.name,
        children: null,
        isLeaf: true
      })) : [],
      data: {
        id: ""
      }
    }] as Array<any>;

    if (!this.setting.onGetTargetList) {
      this.datasetTree = datasetTree;
      return;
    }

    const targetList = await this.setting.onGetTargetList();

    if (targetList && targetList.length > 0) {
      datasetTree = datasetTree.concat(targetList.map(cur => {
        const list = grouped[cur.id];
        const children = list ?
          list.map(data => {
            return {
              label: data.name,
              data
            }
          }) : [];

        return {
          label: cur.title,
          children,
          isLeaf: false,
          data: cur
        }
      }));
    }
    this.datasetTree = datasetTree;
  }

  async handleSubmit() {
    if (!this.setting.onModifyDataSet || !this.setting.onGetDataSet) return;
    await this.setting.onModifyDataSet(this.form as IDataSet)
    this.isEditing = false;
    const res = await this.setting.onGetDataSet();
    await this.refresh(res);
  }

  mounted() {
    this.refresh(this.setting.datasetList || []);
  }
}
</script>
