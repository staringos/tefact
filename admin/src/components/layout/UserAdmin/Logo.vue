<template>
  <div class="title-wrapper" @click="handleClick">
    <LogoImage />
    <h3 class="title" :style="{ color: color }">{{title || "TEFACT"}}</h3>
  </div>
</template>
<style lang="scss" scoped>
  @import "../../../assets/styles/variables";

  .title-wrapper {
    align-items: center;
    display: flex;
    justify-content: center;
    height: 100%;
    margin-left: 30px;
    margin-right: 50px;
    color: #323233;
    cursor: pointer;

    .title {
      font-size: 20px;
      color: white;
      font-weight: 700;
      margin-left: 20px;
      padding-left: 20px;
      border-left: 2px solid $borderColor;
    }
  }
</style>
<script lang="ts">
  import { Component, Vue, Prop } from 'nuxt-property-decorator'
  import LogoImage from '../LogoImage.vue'

  @Component({
    components: { LogoImage }
  })
  export default class Logo extends Vue {
    @Prop(String) title!: String | null
    @Prop(String) color!: String | null
    @Prop(String) direct!: String | null

    handleClick() {
      if (this.direct) {
        location.href = this.direct as any
      }
    }
  }
</script>
