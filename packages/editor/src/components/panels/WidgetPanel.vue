<template>
  <BasePanel class="config-panel">
    <el-tabs v-model="activeName" type="card" @tab-click="handleClick">
      <el-tab-pane label="自定义" name="custom">自定义</el-tab-pane>
      <el-tab-pane label="公共" name="public">公共</el-tab-pane>
    </el-tabs>
  </BasePanel>
</template>
<style lang="scss" scoped>

</style>
<script lang="ts">
import { Vue, Component } from 'nuxt-property-decorator'
import BasePanel from "TEFACT_EDITOR/components/panels/BasePanel.vue";

@Component({
  components: {
    BasePanel
  }
})
export default class WidgetPanel extends Vue {
  activeName="custom"

  handleClick() {}
}
</script>
