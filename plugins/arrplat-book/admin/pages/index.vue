<template>
  <div>
    THis is crm index page
  </div>
</template>

<script lang="ts">
  import { Component, Vue } from 'nuxt-property-decorator'
  import Dashboard from '~/components/Dashboard.vue'

  @Component({
    components: { Dashboard },
    layout: 'plugin'
  })
  export default class Index extends Vue {
  }
</script>
