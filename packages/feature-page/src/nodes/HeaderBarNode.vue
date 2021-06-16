<template>
  <SlotWrapper
    :className="{'header-bar-node': true}"
    v-bind="$attrs"
    v-on="$listeners"
    :node="node"
    :preview="preview"
  >
    <div class="left-area">
      <SlotArea :preview="preview" />
    </div>
    <div class="title-area">{{nodeData.title}}</div>
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
import { Vue, Component, Prop } from 'vue-property-decorator'
import SlotArea from "../components/SlotArea.vue"
import NodeClass from "../nodes/NodeClass"
import { FreeNodeData, getBaseNode, IBaseNode } from "@tefact/core"
import { PageProperties } from "../config"
import SlotWrapper from "../components/SlotWrapper.vue"

@Component({
  components: { SlotWrapper, SlotArea }
} as any)
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
      title: "首页"
    } as FreeNodeData,
  } as any;

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
        title: "导航设置",
        rows: [
          {
            type: "TextRow",
            params: {
              title: "标题",
              path: "data.title",
            },
          }
        ],
      },
    },
  ], ["PositionProperties", "TextProperties"]);

}
</script>
