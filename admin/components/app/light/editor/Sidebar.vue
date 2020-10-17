<template>
  <div class="editor-side-bar" @click.stop>
    <div class="base-resolu" v-if="config.hasTab">
      <el-tabs type="border-card">
        <el-tab-pane
          :label="tab.title"
          v-for="(tab, i) in config.tabs"
          :key="i"
        >
          <el-collapse :value="tab.components.map((component, i) => i)">
            <component
              v-for="(component, i) in tab.components"
              :key="i"
              :index="i"
              :is="component.type"
              :nodeType="nodeType"
              v-bind="component.params"
              :node="nodeData"
              :sectionId="sectionId"
            ></component>
          </el-collapse>
        </el-tab-pane>
      </el-tabs>
    </div>
  </div>
</template>
<style lang="scss" scoped>
  @import "../../../../assets/styles/variables";

  .editor-side-bar {
    flex: 1;
    background: white;
    display: flex;

    .base-resolu {
      display: flex;
      flex: 1;
      flex-direction: column;

      .title {
        display: flex;
        background: $bg-02;
      }
    }

    /deep/ .el-tabs {
      flex: 1;
      box-shadow: none;
      margin-top: -1px;
    }
  }
</style>
<script lang="ts">
  import { Vue, Component, namespace, Prop } from 'nuxt-property-decorator'
  import { NodeResoluConfig } from '~/utils/constants/Editor'
  import { BaseNodeModel } from '~/utils/entities/editor/node'
  import Resolu from './resolu'
  const editor = namespace('editor')

  @Component({
    components: Resolu
  })
  export default class ResoluContainer extends Vue {
    NodeResoluConfig = NodeResoluConfig
    activeCard = []

    @Prop() sectionId

    @editor.Getter currentNode
    @editor.Getter currentPageSection
    @editor.Getter currentPage

    get collapseValue() {
      return
    }

    get nodeData() {
      if (this.currentNode) return this.currentNode
      if (this.currentPageSection) return this.currentPageSection
      return this.currentPage
    }

    get nodeType() {
      if (this.currentNode) {
        return this.currentNode.type
      }

      if (this.currentPageSection) {
        return 'section'
      }

      return 'page'
    }

    get config() {
      return this.NodeResoluConfig[this.nodeType]
    }
  }
</script>
