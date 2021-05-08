<template>
  <BasePanel class="config-panel" title="模版组件">
    <el-tabs v-model="activeName" type="card" @tab-click="handleClick">
      <el-tab-pane label="自定义" name="custom">
        <ul v-if="list && list.length > 0">
          <li v-for="(item, i) in list" :key="item.id">{{item.name}}</li>
        </ul>
        <p v-else style="font-size: 12px; color: #a0a0a0;">在编辑器中，选择组件右键，添加模版组件</p>
      </el-tab-pane>
      <el-tab-pane label="公共" name="public">公共</el-tab-pane>
    </el-tabs>
  </BasePanel>
</template>
<style lang="scss" scoped>

</style>
<script lang="ts">
import { Vue, Component } from 'nuxt-property-decorator'
import BasePanel from "TEFACT_EDITOR/components/panels/BasePanel.vue";
import { BaseView } from "@tefact/core"

@Component({
  components: {
    BasePanel
  }
})
export default class WidgetPanel extends BaseView {
  activeName="custom";
  list: Array<any> = [];

  handleClick() {}

  async mounted() {
    this.list = await this.setting.onGetWidgetList();
  }
}
</script>
