<template>
  <div class="entity-preview">
    <el-table
      :data="data"
      height="250"
      border
      style="width: 100%">
      <el-table-column
        v-for="column in columns"
        :prop="column.key"
        :label="column.key">
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
  import { Vue, Component, Prop, Watch } from 'nuxt-property-decorator'

  @Component
  export default class EntityEditor extends Vue {
    @Prop() data
    columns: any[] = []

    @Watch("data")
    handleDataChange() {
      const { data } = this
      if (!data || data.length === 0) return
      const columns = [] as any
      debugger;
      for (let key in data) {
        columns.push({ key })
      }

      this.columns = columns;
    }
  }
</script>
