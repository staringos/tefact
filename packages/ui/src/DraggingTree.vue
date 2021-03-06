<template>
  <div class="tree-wrapper">
    <DraggingTreeLeaf
      v-for="item in data"
      :item="item"
      :level="0"
      :key="item.id"
    ></DraggingTreeLeaf>
  </div>
</template>
<style lang="scss" scoped>
.tree-wrapper {
  display: flex;
  width: 100%;
  flex: 1;
  flex-direction: column;
}
</style>
<script lang="ts">
import { Vue, Component, Prop } from "vue-property-decorator";
import DraggingTreeLeaf from "./DraggingTreeLeaf.vue";

export interface IDraggingTree {
  id: string | number;
  label: string | number;
  active: boolean;
  children: Array<IDraggingTree>;
}

@Component({
  components: {
    DraggingTreeLeaf,
  },
})
export default class DraggingTree extends Vue {
  @Prop() data!: IDraggingTree;

  handleUpdate(e: Array<string>): void {
    this.$emit("input", `https://${e[0]}`);
  }
}
</script>
