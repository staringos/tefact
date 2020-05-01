<template>
  <div :class="`section ${active ? 'active' : ''}`" @click="handleSectionClick">
    <div class="add-button">
      <i class="el-icon-plus"></i>
    </div>

    <component
      v-for="(node, i) in section.nodes"
      :key="i"
      :node="node"
      :is="NodeTypeToComponent[node.type]"
      @onRefLineChange="handleRefLineChange"
    >

    </component>

    <!--辅助线-->
    <span class="ref-line v-line"
          v-for="item in vLine"
          v-show="item.display"
          :style="{ left: item.position, top: item.origin, height: item.lineLength}"></span>
    <span class="ref-line h-line"
          v-for="item in hLine"
          v-show="item.display"
          :style="{ top: item.position, left: item.origin, width: item.lineLength}"></span>
    <!--辅助线END-->
  </div>
</template>
<style lang="scss" scoped>
  @import "../../../../assets/styles/variables";

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

</style>
<script lang="ts">
  import { Vue, Component, Prop } from 'nuxt-property-decorator'
  import TextNode from './nodes/TextNode.vue'

  import { NodeTypeToComponent } from '~/utils/constants/Editor'

  @Component({
    components: {
      TextNode
    }
  })
  export default class AppItem extends Vue {
    @Prop() section
    @Prop([Boolean]) active!: boolean

    NodeTypeToComponent = NodeTypeToComponent

    vLine = []
    hLine = []

    handleRefLineChange(params) {
      const { vLine, hLine } = params
      this.vLine = vLine
      this.hLine = hLine
    }

    handleSectionClick() {
      this.$emit("onActiveChange")
    }

    mounted() {
      console.log("section:", this.section)
    }
  }
</script>
