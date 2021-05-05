<template>
  <SlotWrapper
    v-bind="$attrs"
    v-on="$listeners"
    :className="{ 'tab-bar-container': true, 'tab-bar-editing': !preview }"
    :node="node"
  >
    <ul>
      <li v-for="(tab, i) in nodeData.tabs" :key="i" @click="handleSwitch(tab)">
        <i v-if="!tab.icon.startsWith('https')" :class="`el-icon ${tab.icon}`"></i>
        <img v-else :src="tab.icon" />
        <span>{{ tab.name }}</span>
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
      tabs: [
        {
          icon: 'el-icon-s-home',
          link: 'el-icon-s-home',
          name: '首页'
        }, {
          icon: 'el-icon-s-home',
          link: 'el-icon-s-home',
          name: '新闻'
        }, {
          icon: 'el-icon-s-home',
          link: 'el-icon-s-home',
          name: '我的'
        }
      ]
    } as FreeNodeData,
  } as any;

  static NODE = {
    icon: "tf-icon-tab",
    type: "TabBarNode",
    position: "slot",
    slot: "TabBar",
    title: "底部导航",
    nodeData: TabBarNode.DEFAULT,
  };

  static PROPERTIES = PageProperties.defaultProperties("底部导航栏", [
    {
      type: "ListProperties",
      params: {
        title: "导航设置",
        path: "data.tabs",
        rows: [
          {
            type: "TextRow",
            params: {
              title: "标题",
              path: "name",
            },
          },
          {
            type: "TextRow",
            params: {
              title: "图标",
              path: "icon",
            },
          },
          {
            type: "SelectRow",
            require: true,
            params: {
              title: "类型",
              path: "type",
              selectOptions: [
                { value: "jump", label: "跳转链接" },
                { value: "page", label: "页面" },
              ],
            },
          },
          {
            type: "TextRow",
            condition: (cur) => {
              return cur.type === "jump"
            },
            params: {
              title: "链接",
              path: "link",
            },
          },
          {
            type: "TargetSelectRow",
            condition: (cur) => {
              return cur.type && cur.type !== "jump"
            },
            params: {
              title: "页面",
              path: "pageId",
              targetFeatureType: "page"
            } as any,
          }
        ],
      }
    }
  ], null, ["PositionProperties", "TextProperties"]);

  handleSwitch(tab) {
    if (!this.preview) {
      return this.$message.warning("编辑状态下，不可跳转");
    }

    this.engine.goto(tab.type, tab.type === 'link' ? tab.link : tab.pageId);
  }
}
</script>
