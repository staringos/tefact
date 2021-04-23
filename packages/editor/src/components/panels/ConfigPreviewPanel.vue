<template>
  <BasePanel class="config-panel" title="配置">
    <json-viewer
      :value="currentTarget"
      :expand-depth="5"
      copyable
      sort
    ></json-viewer>
  </BasePanel>
</template>
<style lang="scss" scoped>
.config-panel {
  ::v-deep.jv-container {
    height: 100%;
    border: 0;
    border-radius: 0;

    .jv-code {
      width: 100%;
      padding-left: 5px;
      padding-right: 5px;
      overflow-x: auto;
    }
  }
}
</style>
<script lang="ts">
import { Vue, Component } from "vue-property-decorator";
import "vue-json-viewer/style.css";
import BasePanel from "TEFACT_EDITOR/components/panels/BasePanel.vue";
import { BaseView } from "@tefact/core";

@Component({
  components: {
    JsonViewer: () => process.client ? import("vue-json-viewer") : Promise.resolve({ render: (h) => h('div') }),
    BasePanel
  }
})
export default class ConfigPreviewPanel extends BaseView {
  get jsonData() {
    return JSON.stringify(this.currentTarget)
  }
}
</script>