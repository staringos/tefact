<template>
  <div class="editor-page-canvas">
    <div :class="`section ${active === section.id ? 'active' : ''}`" v-for="section in sections" :key="id" @click="handleSectionClick(section)">

      <div class="add-button">
        <i class="el-icon-plus"></i>
      </div>
    </div>
  </div>
</template>
<script lang="ts">
  import { Vue, Component } from 'nuxt-property-decorator'

  @Component
  export default class AppItem extends Vue {
    sections = [{
      id: 1,
    }, {
      id: 2,
    }]

    active = null

    handleSectionClick(section) {
      this.active = section.id
    }
  }
</script>

<style lang="scss" scoped>
  @import "../../../../assets/styles/variables";

  .editor-page-canvas {
    width: 80%;
    min-height: 500px;
    display: flex;
    flex-direction: column;
    background: white;
    margin: 0 auto;
    box-shadow: 0 2px 4px 0 rgba(0,0,0,.12), 0 0 6px 0 rgba(0,0,0,.04);

    .section {
      flex: 1;
      min-height: 300px;
      position: relative;

      &:hover, &.active {
        border: 1px solid $editor-border-active-color;
      }

      &:hover {
        .add-button {
          display: flex;
        }
      }
    }

    .add-button {
      display: none;
      width: 50px;
      height: 50px;
      border-radius: 50%;
      background-color: $editor-main-color;
      margin: 0 auto;
      position: absolute;
      bottom: -25px;
      justify-content: center;
      align-items: center;
      left: 50%;
      margin-left: -25px;
      cursor: pointer;

      .el-icon-plus {
        color: white;
        font-weight: bold;
        font-size: 16px;
      }
    }
  }
</style>
