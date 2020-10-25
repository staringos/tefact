<template>
  <ArrPanel style="margin: 0; flex: 1;" title="数据表" headerButton="el-icon-plus" border header>
    <el-table
      ref="multipleTable"
      :data="tableList"
      tooltip-effect="dark"
      style="width: 100%"
      size="mini"
      :show-header="false"
      @selection-change="handleSelectionChange">
      <el-table-column
        prop="name"
        label="姓名">
      </el-table-column>
    </el-table>
  </ArrPanel>
</template>
<style lang="scss">

</style>
<script lang="ts">
  import { Vue, Component, Prop } from 'nuxt-property-decorator'

  @Component
  export default class AppItem extends Vue {
    @Prop() tableList

    handleSelectionChange(e) {
      this.$emit("input", e.id)
    }
  }
</script>
