<template>
  <div class="entity-editor-panel">
    <el-select v-model="value" placeholder="请选择数据实体">
      <el-option
        v-for="item in options"
        :key="item.value"
        :label="item.label"
        :value="item.value">
      </el-option>
    </el-select>
  </div>
</template>
<style lang="scss" scoped>
  @import "../../../../assets/styles/variables";

  .entity-editor-panel {
    height: 100px;
    background: white;
    border: 1px solid $borderColor;
    padding: 15px;
  }
</style>
<script lang="ts">
  import { Vue, Component } from 'nuxt-property-decorator'

  @Component
  export default class EntityEditor extends Vue {
    options: Object[] = [{
      value: '选项1',
      label: '黄金糕'
    }, {
      value: '选项2',
      label: '双皮奶'
    }, {
      value: '选项3',
      label: '蚵仔煎'
    }, {
      value: '选项4',
      label: '龙须面'
    }, {
      value: '选项5',
      label: '北京烤鸭'
    }]

    value: String = ''
  }
</script>
