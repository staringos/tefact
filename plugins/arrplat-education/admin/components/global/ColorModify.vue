<template>
  <div>
    <Compact v-model="colors" />
  </div>
</template>
<style lang="scss">

</style>
<script lang="ts">
  import { Vue, Component, Prop, Watch, Emit } from 'nuxt-property-decorator'
  import { Compact } from 'vue-color'

  @Component({
    components: {
      Compact
    }
  })
  export default class ColorModify extends Vue {
    @Prop() field
    @Prop() row

    colors = '#194d33' as any

    @Watch('colors')
    @Emit('change')
    onColorChange() {
      let hex = this.colors
      if (this.colors.hex) {
        hex = hex.hex
      }

      return { [this.field.key]: hex }
    }

    mounted() {
      const color = this.row[this.field.key]
      if (color && color.length > 1) {
        this.colors = color
      }
    }
  }
</script>
