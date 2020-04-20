<template>
  <div class="desktop">
    <img class="background" src="/bg.jpg"/>
    <div class="content">
      <Dashboard />
    </div>
  </div>
</template>
<script lang="ts">
  import { Component, Vue } from 'nuxt-property-decorator'
  import Dashboard from '~/components/Dashboard.vue'

  @Component({
    components: { Dashboard },
    layout: 'UserAdmin'
  })
  export default class Index extends Vue {
  }
</script>
<style lang="scss">
  .desktop {
    position: relative;
    background: #6aaafd;
    display: flex;
    flex: 1;
    height: 100%;

    .background {
      height: 100%;
      width: 100%;
    }

    .content {
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      padding-top: 100px;
    }
  }
</style>
