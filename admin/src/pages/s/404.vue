<template>
  <div>
    <span>页面未找到</span>
  </div>
</template>
<style lang="scss">

</style>
<script lang="ts">
import { Vue, Component } from 'nuxt-property-decorator'

@Component({
  layout: "Share"
})
export default class AppItem extends Vue {
  id = null
}
</script>
