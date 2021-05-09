<template>
  <BasePanel class="config-panel" title="模版组件">
    <el-tabs v-model="activeName" @tab-click="handleClick">
      <el-tab-pane label="自定义" name="custom">
        <ul class="widget-list" v-if="list && list.length > 0">
          <li
            class="widget-item"
            v-for="(item, i) in list" :key="item.id"
            @click="handleClick(item)"
          >
            <div class="head-image">
              <i class="tefact-icon tf-icon-modelbim"/>
            </div>
            <p class="widget-name">{{item.name}}</p>
            <i class="el-icon-delete" @click.stop="handleDelete(item)"></i>
          </li>
        </ul>
        <p v-else style="font-size: 12px; color: #a0a0a0;">在编辑器中，选择组件右键，添加模版组件</p>
      </el-tab-pane>
      <el-tab-pane label="公共" name="public">公共</el-tab-pane>
    </el-tabs>
  </BasePanel>
</template>
<style lang="scss" scoped>
.widget-list {
  display: flex;
  flex-direction: row;
  flex-flow: row wrap;
  margin: 5px 0 0 5px;

  .widget-item {
    width: 70px;
    min-height: 50px;
    border-radius: 3px;
    margin-right: 5px;
    list-style: none;
    position: relative;
    cursor: pointer;

    .head-image {
      width: 70px;
      display: flex;
      justify-content: center;
      align-items: center;
      min-height: 50px;
      color: $mainColor;
    }
  }

  .el-icon-delete {
    display: none;
  }

  .widget-name {
    height: 36px;
    line-height: 36px;
    padding: 0 5px;
    font-size: 12px;
    text-align: center;
  }

  .widget-item:hover {
    .el-icon-delete {
      display: block;
      position: absolute;
      top: 1px;
      right: 1px;
      width: 20px;
      text-align: center;
      height: 20px;
      background: white;
      font-size: 12px;
      border-bottom-left-radius: 50%;
      line-height: 20px;
      color: #333;
    }
  }
}
</style>
<script lang="ts">
import { Vue, Component } from 'nuxt-property-decorator'
import BasePanel from "TEFACT_EDITOR/components/panels/BasePanel.vue";
import { BaseView } from "@tefact/core"
import cloneDeep from 'lodash/cloneDeep'

@Component({
  components: {
    BasePanel
  }
})
export default class WidgetPanel extends BaseView {
  activeName="custom";
  list: Array<any> = [];

  handleClick(item) {
    let parentId = undefined as any;
    let node = cloneDeep(item.config);

    node.pos.x = 10;
    node.pos.y = 10;

    if (this.activeNodeId) {
      if (this.activeNodeType === "section") parentId = this.activeNodeId;
      else parentId = this.engine.activatedNodeParentId;
    }

    if (this.featureType === "form") return this.engine.add(node, -1);
    this.engine.addNode(node, parentId);
  }

  async handleDelete(item) {
    await this.setting.onDeleteWidget(item.id);
    this.refresh();
  }

  async refresh() {
    this.list = await this.setting.onGetWidgetList();
  }

  async mounted() {
    this.refresh();
  }
}
</script>
