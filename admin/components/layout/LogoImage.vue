<template>
  <div class="logo">
    <img src="../../assets/images/icon-logo.png" />
  </div>
</template>
<script lang="ts">
  import { Component, Vue } from 'nuxt-property-decorator'

  @Component({})
  export default class Logo extends Vue {}
</script>
<style lang="scss" scoped>
  .logo {
    img {
      margin: 0 auto;
      height: 45px;
    }
  }
</style>
