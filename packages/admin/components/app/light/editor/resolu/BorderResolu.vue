<template>
  <BaseResolu title="边框设置" v-bind="$attrs">
    <span>This is Position </span>
  </BaseResolu>
</template>
<style lang="scss">

</style>
<script lang="ts">
  import { Vue, Component } from "nuxt-property-decorator";
  import BaseResolu from '~/components/app/light/editor/resolu/BaseResolu.vue'

  @Component({
    components: { BaseResolu }
  })
  export default class BorderResolu extends Vue {

  }
</script>
