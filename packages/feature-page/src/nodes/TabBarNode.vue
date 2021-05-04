<template>
  <div :class="{ 'tab-bar-container': true, 'tab-bar-editing': !preview }">
    <ul>
      <li>
        <i class="el-icon el-icon-s-home"></i>
        <span>首页</span>
      </li>
      <li>
        <i class="el-icon el-icon-s-home"></i>
        <span>首页</span>
      </li>
      <li>
        <i class="el-icon el-icon-s-home"></i>
        <span>首页</span>
      </li>
    </ul>
  </div>
</template>
<style lang="scss" scoped>
.tab-bar-container {
  height: 50px;
  width: 100%;
  display: flex;
  position: absolute;
  bottom: 0;
  left: 0;
  background-color: white;
  border-top: 1px solid $borderColor;
  flex: 1;
  z-index: 999;
  box-sizing: border-box;

  &.tab-bar-editing:hover {
    border: 1px solid $editor-border-active-color;
  }

  ul{
    display: flex;
    flex: 1;
    height: 100%;

    li {
      flex: 1;
      display: flex;
      justify-content: center;
      align-items: center;
      flex-direction: column;
      font-size: 12px;
      cursor: pointer;
      .el-icon {
        font-size: 22px;
      }
    }
  }
}
</style>
<script lang="ts">
import { Component, Vue, Prop } from "vue-property-decorator";
import NodeClass from "./NodeClass";
import BaseNode from "./BaseNode.vue";
import shapes from "../shapes";
import type { IBaseNode } from "@tefact/core";

@Component({
  components: { BaseNode, ...shapes },
})
export default class TabBarNode extends NodeClass<IBaseNode> {
  @Prop() preview;

}
</script>
