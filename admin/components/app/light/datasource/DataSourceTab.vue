<template>
  <ArrPanel style="margin: 0; height: 200px; flex: none;" title="数据源" headerButton="el-icon-plus" @on-header-button-click="() => handleClick(false)" border header>
    123 4444
  </ArrPanel>
</template>
<style lang="scss">
  /deep/ .data-source-tab {
    margin: 0;
    height: 100px;
  }
</style>
<script lang="ts">
  import { Vue, Component } from 'nuxt-property-decorator'

  @Component
  export default class DataSourceTab extends Vue {

    handleClick() {}
  }
</script>
