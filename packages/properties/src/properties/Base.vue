<template>
  <el-collapse-item :title="title" :name="index">
    <slot></slot>
  </el-collapse-item>
</template>
<style lang="scss">
@import "~@tefact/core/src/variables.scss";

.base-resolu {
  display: flex;

  ::v-deep .el-tabs__content {
    padding-top: 0;

    ::v-deep .el-collapse {
      border-top: 0;
    }
  }

  .resolu-title {
    background: $gray-01;
    min-height: 30px;
    line-height: 43px;
    padding-left: 27px;
  }
}
</style>
<script lang="ts">
import { Vue, Component, Prop } from "vue-property-decorator";

@Component
export default class BaseProperties extends Vue {
  @Prop() title?: string;
  @Prop() index?: number;
}
</script>
