<template>
  <div :style="`border: 1px solid #e3e3e3; background-color: ${row && field && row[field.key]}; width: 60px; height: 30px;`">
  </div>
</template>
<style lang="scss">

</style>
<script lang="ts">
  import { Vue, Component, Prop } from 'nuxt-property-decorator'

  @Component
  export default class AppItem extends Vue {
    @Prop() field
    @Prop() row
  }
</script>
