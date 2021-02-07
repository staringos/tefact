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
}
</style>
<script lang="ts">
import { Vue, Component, Prop } from "vue-property-decorator";
import LayersPanel from "@/components/panels/LayersPanel.vue";
import NodeListPanel from "@/components/panels/NodeListPanel.vue";
import { TargetFeatureType } from "@tefact/common";

@Component({
  components: { NodeListPanel, LayersPanel }
})
export default class NodesBar extends Vue {
  @Prop() featureType?: TargetFeatureType;
}
</script>
