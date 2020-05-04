<template>
  <BaseResolu title="文字设置" v-bind="$attrs">
    <span>This is colleape</span>
  </BaseResolu>
</template>
<style lang="scss">

</style>
<script lang="ts">
  import { Vue, Component, Prop } from 'nuxt-property-decorator'
  import BaseResolu from '~/components/app/light/editor/resolu/BaseResolu.vue'

  @Component({
    components: { BaseResolu }
  })
  export default class TextResolu extends Vue {
  }
</script>
