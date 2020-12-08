<template>
  <div class="form-node-wrapper">
    <el-input v-model="input" placeholder="请输入内容"></el-input>
  </div>
</template>
<style lang="scss">
  @import "./style.scss";
</style>
<script lang="ts">
import { Vue, Component } from 'nuxt-property-decorator'

@Component
export default class InputNode extends Vue {
  input = ""
}
</script>
