<template>
  <div class="title-wrapper">
    <LogoImage />
    <h3 class="title">Arrplat</h3>
  </div>
</template>
<style lang="scss" scoped>
  @import "../../../assets/styles/variables";

  .title-wrapper {
    align-items: center;
    display: flex;
    justify-content: center;
    height: 100%;
    margin-left: 30px;
    margin-right: 50px;
    color: #323233;

    .title {
      font-size: 20px;
      color: #323233;
      font-weight: 700;
      margin-left: 20px;
      padding-left: 20px;
      border-left: 2px solid $borderColor;
    }
  }
</style>
<script lang="ts">
  import { Component, namespace, Vue } from 'nuxt-property-decorator'
  import LogoImage from '../LogoImage.vue'

  @Component({
    components: { LogoImage }
  })
  export default class Logo extends Vue {

  }
</script>
