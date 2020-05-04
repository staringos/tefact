<template>
  <div style="width: 100%;">
    <h3>{{section.title}}</h3>

  </div>
</template>
<script lang="ts">
  import { Component, Vue, Prop } from 'nuxt-property-decorator'
  import { EntityPageSection } from '@arrplat/common'
  import List from './List.vue'

  @Component({
    components: { List }
  })
  export default class PageSection extends Vue {
    @Prop() section: EntityPageSection
  }
</script>
