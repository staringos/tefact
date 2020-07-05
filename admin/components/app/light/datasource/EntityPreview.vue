<template>
  <div class="entity-preview">
    <el-table
      :data="tableData"
      height="250"
      border
      style="width: 100%">
      <el-table-column
        prop="date"
        label="日期"
        width="180">
      </el-table-column>
      <el-table-column
        prop="name"
        label="姓名"
        width="180">
      </el-table-column>
      <el-table-column
        prop="address"
        label="地址">
      </el-table-column>
    </el-table>
  </div>
</template>
<style lang="scss">
.entity-preview {
  display: flex;
  flex: 1;
  flex-direction: column;

  .el-table {
    flex: 1;
  }
}
</style>
<script lang="ts">
  import { Vue, Component } from 'nuxt-property-decorator'

  @Component
  export default class EntityEditor extends Vue {

  }
</script>
