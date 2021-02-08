import { Vue, Component, Prop } from 'vue-property-decorator';
import { BaseView, IBaseNode } from "@tefact/core"

@Component
export default class NodeClass<T extends IBaseNode> extends BaseView {
  @Prop() public sectionId!: string
  @Prop() public node!: T
  @Prop() public preview!: boolean

  get nodeData() {
    return this.node?.data || {} as any
  }

  get config() {
    return this.node || {} as any
  }

  // node 配置
  NODE = {}

  // 属性设置面板配置
  PROPERTIES = {}

  // 默认值配置
  DEFAULT = {}
}
