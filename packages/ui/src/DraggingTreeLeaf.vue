<template>
  <div class="tree-wrapper-leaf">
    <div class="current-panel">
      <span>{{ item.label }}</span>
    </div>
    <div class="children-panel" v-if="item.children.length > 0">
      <DraggingTreeLeaf
        v-for="item in item.children"
        :level="level + 1"
        :item="item"
        :key="item.id"
      ></DraggingTreeLeaf>
    </div>
  </div>
</template>
<style lang="scss" scoped>
.tree-wrapper-leaf {
  display: flex;
  flex-direction: column;
  .current-panel {
    height: 35px;
    width: 100%;
  }
}
</style>
<script lang="ts">
import { Vue, Component, Prop } from "vue-property-decorator";
import type { IDraggingTree } from "./DraggingTree.vue";

@Component({
  components: {
    DraggingTreeLeaf,
  },
})
export default class DraggingTreeLeaf extends Vue {
  @Prop() item!: IDraggingTree;
  @Prop() level!: number;

  handleUpdate(e: Array<string>): void {
    this.$emit("input", `https://${e[0]}`);
  }
}
</script>
