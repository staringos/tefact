<template>
  <div :class="`section ${active ? 'active' : ''}`" @click="handleSectionClick">
    <AddButton :index="index"></AddButton>

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
    background-color: white;

    &:hover, &.active {
      border: 1px solid $editor-border-active-color;
    }

    &:hover {
      /deep/ .add-button {
        display: flex;
      }
    }
  }

</style>
<script lang="ts">
  import { Vue, Component, Prop } from 'nuxt-property-decorator'
  import TextNode from './nodes/TextNode.vue'
  import AddButton from "~/components/app/light/editor/AddButton.vue"

  import { NodeTypeToComponent } from '~/utils/constants/Editor'

  @Component({
    components: {
      TextNode, AddButton
    }
  })
  export default class AppItem extends Vue {
    @Prop() section
    @Prop() index: number = 0
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
