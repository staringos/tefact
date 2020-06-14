<template>
  <div class="card">
    <slot></slot>
  </div>
</template>
<script lang="ts">
  import { Component, Vue } from 'nuxt-property-decorator'

  @Component
  export default class Index extends Vue {

  }
</script>
<style lang="scss" scoped>
  .card {
    transition: all .3s ease-in-out;
    border: none;
    -webkit-box-shadow: 0 4px 25px 0 rgba(0, 0, 0, .1);
    box-shadow: 0 4px 25px 0 rgba(0, 0, 0, .1);
    background: #eff2f7;
  }
</style>
