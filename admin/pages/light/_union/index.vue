<template>
  <ArrPanel v-if="currentApp" :title="currentApp.title" border>
    <p>轻应用默认首页</p>
  </ArrPanel>
</template>
<style lang="scss">

</style>
<script lang="ts">
  import { Vue, Component, namespace } from 'nuxt-property-decorator'

  const app = namespace('app')

  @Component({
    layout: 'plugin'
  })
  export default class AppItem extends Vue {
    @app.Getter currentApp
  }
</script>
