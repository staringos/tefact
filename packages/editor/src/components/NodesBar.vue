<template>
  <div class="nodes-bar">
    <NodeListPanel :featureType="featureType" />
    <LayersPanel :featureType="featureType" />
  </div>
</template>
<style lang="scss" scoped>
.nodes-bar {
  display: flex;
  width: 160px;
  flex-direction: column;
  position: relative;

  &.collapse {
    width: 0px;
    max-width: 0px;
  }

  .collapse-control {
    width: 12px;
    height: 50px;
    color: #e2e8f0;
    border: 1px solid #e2e8f0;
    display: flex;
    text-align: center;
    align-items: center;
    justify-content: center;
    position: absolute;
    top: 50%;
    right: -10px;
    margin-top: -25px;
    background: white;
    z-index: 999;
    border-radius: 2px;
  }
}
</style>
<script lang="ts">
import { Vue, Component, Prop } from "vue-property-decorator";
import LayersPanel from "TEFACT_EDITOR/components/panels/LayersPanel.vue";
import NodeListPanel from "TEFACT_EDITOR/components/panels/NodeListPanel.vue";
import type { TargetFeatureType } from "@tefact/core";
import { CollapseButton } from "@tefact/ui";

@Component({
  components: { NodeListPanel, LayersPanel, CollapseButton }
})
export default class NodesBar extends Vue {
  @Prop() featureType?: TargetFeatureType;
}
</script>
