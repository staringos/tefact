<template>
  <div
    class="add-button"
    v-show="show"
    @click="handleAddPageSection">
    <i class="el-icon-plus"></i>
  </div>
</template>
<style lang="scss" scoped>
  @import "../../../../assets/styles/variables";

  .add-button {
    width: 50px;
    height: 50px;
    border-radius: 50%;
    background-color: $editor-main-color;
    margin: 0 auto;
    // position: absolute;
    // bottom: -25px;
    justify-content: center;
    align-items: center;
    display: flex;
    // left: 50%;
    // margin-left: -25px;
    cursor: pointer;

    .el-icon-plus {
      color: white;
      font-weight: bold;
      font-size: 16px;
    }
  }
</style>
<script lang="ts">
  import { Vue, Component, Prop, namespace } from 'nuxt-property-decorator'

  const editor = namespace('editor')

  @Component
  export default class AddButton extends Vue {
    @Prop() index: number = 0
    @Prop() pageId!: string
    @Prop([Boolean]) show!: boolean

    @editor.Action addPageSection

    handleAddPageSection() {
      this.addPageSection({ index: this.index, pageId: this.pageId })
    }
  }
</script>
