<template>
  <SlotWrapper
    v-bind="$attrs"
    v-on="$listeners"
    :className="{ 'tab-bar-container': true, 'tab-bar-editing': !preview }"
    :node="node"
  >
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
  </SlotWrapper>
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
import { FreeNodeData, getBaseNode } from "@tefact/core";
import { PageProperties } from "../config";
import SlotWrapper from "../components/SlotWrapper.vue"

@Component({
  components: { SlotWrapper, BaseNode, ...shapes },
})
export default class TabBarNode extends NodeClass<IBaseNode> {
  @Prop() preview;

  static DEFAULT = {
    ...getBaseNode(),
    type: "TabBarNode",
    style: {},
    pos: {
      w: null,
      h: null,
      x: null,
      y: null,
    },
    data: {
      dataPath: null
    } as FreeNodeData,
  } as IBaseNode;

  static NODE = {
    icon: "tf-icon-tab",
    type: "TabBarNode",
    position: "slot",
    slot: "TabBar",
    title: "底部导航",
    nodeData: TabBarNode.DEFAULT,
  };

  static PROPERTIES = PageProperties.defaultProperties("底部导航栏", null, [
    {
      type: "RowsProperties",
      params: {
        title: "按钮设置",
        rows: [
          {
            type: "SelectRow",
            params: {
              title: "类型",
              path: "data.type",
              selectOptions: [
                { value: "primary", label: "主要" },
                { value: "info", label: "普通" },
                { value: "warning", label: "警告" },
                { value: "danger", label: "错误" },
                { value: "text", label: "文字" },
                { value: "success", label: "成功" },
              ],
            },
          },
          {
            type: "TextRow",
            params: {
              title: "按钮文字",
              path: "data.text",
            },
          },
          {
            type: "SwitchRow",
            params: {
              title: "朴素按钮",
              path: "data.plain",
            },
          },
          {
            type: "SwitchRow",
            params: {
              title: "圆角",
              path: "data.round",
            },
          },
          {
            type: "SwitchRow",
            params: {
              title: "圆形",
              path: "data.circle",
            },
          },
        ],
      },
    },
  ]);
}
</script>
