<template>
  <div>
    THis is crm customer index page
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
