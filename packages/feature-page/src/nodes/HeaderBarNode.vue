<template>
  <SlotWrapper
    :className="{'header-bar-node': true}"
    v-bind="$attrs"
    v-on="$listeners"
    :node="node"
  >
    <div class="left-area">
      <SlotArea :preview="preview" />
    </div>
    <div class="title-area">{{title}}</div>
    <div class="right-area">
      <SlotArea :preview="preview" />
    </div>
  </SlotWrapper>
</template>
<style lang="scss" scoped>
.header-bar-node {
  display: flex;
  position: absolute;
  top: 0;
  left: 0;
  background-color: white;
  border-bottom: 1px solid $borderColor;
  box-sizing: border-box;
  height: 50px;
  width: 100%;
  align-items: center;
  padding: 5px;

  .left-area, .right-area {
    max-width: 200px;
    width: 100px;
    height: 40px;
  }

  .title-area {
    flex: 1;
    text-align: center;
  }
}
</style>
<script lang="ts">
import { Vue, Component, Prop } from 'nuxt-property-decorator'
import SlotArea from "../components/SlotArea.vue"
import NodeClass from "../nodes/NodeClass"
import { FreeNodeData, getBaseNode, IBaseNode } from "@tefact/core"
import { PageProperties } from "../config"
import SlotWrapper from "../components/SlotWrapper.vue"

@Component({
  components: { SlotWrapper, SlotArea }
})
export default class HeaderBarNode extends NodeClass<IBaseNode> {
  title = "首页"
  @Prop() preview

  static DEFAULT = {
    ...getBaseNode(),
    type: "HeaderBarNode",
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
    icon: "tf-icon-tab1",
    type: "HeaderBarNode",
    position: "slot",
    slot: "HeaderBar",
    title: "顶部导航",
    nodeData: HeaderBarNode.DEFAULT,
  };

  static PROPERTIES = PageProperties.defaultProperties("顶部导航", null, [
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
