<template>
  <el-dialog
      title="数据项管理"
      :visible.sync="value"
      class="page-previewer"
      :before-close="() => $emit('cancel')"
      width="70%"
  >
    <div class="dataset-wrapper">
      <el-tree class="dataset-tree" :data="data" :props="defaultProps" @node-click="handleNodeClick"></el-tree>
      <div class="dataset-modify">
        <el-form v-if="currentDataset" ref="form" :model="form" label-width="80px">
          <el-form-item label="名称">
            <el-input v-model="form.name"></el-input>
          </el-form-item>
          <el-form-item label="活动区域">
            <el-select v-model="form.region" placeholder="请选择活动区域">
              <el-option label="区域一" value="shanghai"></el-option>
              <el-option label="区域二" value="beijing"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="即时配送">
            <el-switch v-model="form.delivery"></el-switch>
          </el-form-item>
          <el-form-item label="特殊资源">
            <el-radio-group v-model="form.resource">
              <el-radio label="线上品牌商赞助"></el-radio>
              <el-radio label="线下场地免费"></el-radio>
            </el-radio-group>
          </el-form-item>
          <el-form-item label="活动形式">
            <el-input type="textarea" v-model="form.desc"></el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="onSubmit">立即创建</el-button>
            <el-button>取消</el-button>
          </el-form-item>
        </el-form>
        <p v-else>请在左侧选择或创建数据项</p>
      </div>
    </div>
  </el-dialog>
</template>
<script lang="ts">
import { Component, Prop } from "vue-property-decorator"
import Previewer from "../common/Previewer.vue";
import SharePageEditor from "../common/SharePageEditor.vue";
import {BaseView} from "../../../../core";

@Component({
  components: { Previewer, SharePageEditor },
})
export default class DataSetDialog extends BaseView {
  @Prop(Boolean) value

  defaultProps = {}
  currentDataset = null

  data = [{
    label: '全局数据项',
    children: [{
      label: '二级 1-1',
      children: [{
        label: '三级 1-1-1'
      }]
    }]
  }, {
    label: '页面1 数据项',
    children: [{
      label: '二级 2-1',
      children: [{
        label: '三级 2-1-1'
      }]
    }, {
      label: '二级 2-2',
      children: [{
        label: '三级 2-2-1'
      }]
    }]
  }, {
    label: '页面2 数据项',
    children: [{
      label: '二级 3-1',
      children: [{
        label: '三级 3-1-1'
      }]
    }, {
      label: '二级 3-2',
      children: [{
        label: '三级 3-2-1'
      }]
    }]
  }];

  handleNodeClick() {}
}
</script>