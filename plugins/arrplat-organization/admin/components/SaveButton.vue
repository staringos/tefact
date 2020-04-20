<template>
  <el-button round class="modify-btn" type="primary" @click="handleClick">
    <slot></slot>
  </el-button>
</template>
<style lang="scss" scoped>
  .modify-btn {
    height: 40px;
    margin-top: 12px;
    margin-left: 20px;
    margin-bottom: 10px;
    float: right;
  }
</style>
<script lang="ts">
  import { Component, Vue, Emit } from 'nuxt-property-decorator'

  @Component
  export default class SaveButton extends Vue {

    @Emit('onClick')
    handleClick(e) {
      return e
    }
  }
</script>
