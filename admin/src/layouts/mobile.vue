<template>
  <div class="mobile-wrapper">
    <nuxt />
  </div>
</template>
<style lang="scss">
  .mobile-wrapper {
  }
</style>
<script lang="ts">
  import { Component, Vue, namespace } from 'nuxt-property-decorator'
  const app = namespace('app')

  @Component({
    components: {}
  })
  export default class Mobile extends Vue {
    props = {}
    data () {
        return {}
    }

    @app.Action('init') init:any
    @app.Getter allOrgs

    created () {
      if (process.server) return
      this.init()
    }
  }
</script>
