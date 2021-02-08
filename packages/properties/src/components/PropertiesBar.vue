<template>
  <div class="editor-side-bar" @click.stop @keydown.stop>
    <div class="base-resolu" v-if="config && config.hasTab">
      <el-tabs type="border-card" v-model="activeTab">
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
<script lang="ts">
import { Component, Prop, Watch } from "vue-property-decorator";
import Properties from "../properties";
import { PROPERTIES_CONFIGS } from "../config";
import { BaseView } from "@tefact/core";
import { EVENT_INSIDE } from "@tefact/core";

// const editor = namespace('editor')

@Component({
  components: Properties,
})
export default class PropertiesContainer extends BaseView {
  NodeResoluConfig = PROPERTIES_CONFIGS;
  activeCard = [];
  activeTab = "0";

  // @editor.Getter currentNode;
  // @editor.Getter currentSection;
  // @editor.Getter currentPage;
  // @editor.Getter isFormGetter;

  get nodeData() {
    if (this.activeNode) return this.activeNode;
    return this.currentTarget;
  }

  get nodeType(): string {
    if (this.activeNode) {
      return this.activeNode.type;
    }

    return "page";
  }

  get config() {
    if (this.isForm && this.nodeType === "page") {
      return this.NodeResoluConfig["FormPage"];
    }
    return this.NodeResoluConfig[this.nodeType];
  }

  @Watch("currentNode")
  handleCurrentNodeChange() {
    this.activeTab = "0";
  }

  mounted() {
    const that = this as any;
    that.$bus.$on(EVENT_INSIDE.SWITCH_PROPERTIES_TAB, (msg: string) => {
      this.activeTab = msg;
    });
  }
}
</script>
<style lang="scss" scoped>
@import "~@tefact/core/src/variables.scss";

.editor-side-bar {
  flex: 1;
  background: white;
  display: flex;
  max-width: 325px;

  .base-resolu {
    display: flex;
    flex: 1;
    flex-direction: column;
    max-width: 100%;

    .title {
      display: flex;
      background: $bg-02;
    }
  }

  ::v-deep .el-tabs {
    flex: 1;
    box-shadow: none;
    margin-top: -1px;
    height: 100%;
    display: flex;
    flex-direction: column;

    .el-tab-pane {
      height: 100%;
      display: flex;
      overflow: auto;
    }

    .el-tabs__content {
      flex: 1;
      height: 0;

      .el-collapse {
        width: 100%;
      }
    }
  }
}
</style>
