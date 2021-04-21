<template>
  <div class="collapse-control" @click="handleCollapse">
    <i class="el-icon-arrow-right" v-if="value"></i>
    <i class="el-icon-arrow-left" v-else></i>
  </div>
</template>
<style lang="scss" scoped>
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
</style>
<script lang="ts">
import { Vue, Component, Prop } from "vue-property-decorator";

@Component({
  components: {}
})
export default class CollapseButton extends Vue {
  @Prop(Boolean) value;

  handleCollapse() {
    this.$emit("input", !this.value);
  }
}
</script>