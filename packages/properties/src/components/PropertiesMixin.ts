import { Component, Prop, Watch } from 'vue-property-decorator'
import cloneDeep from 'lodash/cloneDeep'
import { BaseNodeStyle, BaseView, DefaultNodeData, IBaseNode } from '@tefact/core'

@Component
export default class PropertiesMixin extends BaseView {
  @Prop() public node!: IBaseNode
  @Prop() public nodeType!: string

  public tmpNode!: IBaseNode

  public init() {
    if (!this.node) return
    const tmpNode = cloneDeep(this.node)
    if (!tmpNode && DefaultNodeData[this.featureType])
      this.tmpNode = DefaultNodeData[this.featureType]

    if (tmpNode && !tmpNode.style)
      tmpNode.style = BaseNodeStyle

    this.tmpNode = tmpNode
  }

  @Watch('node', { deep: true, immediate: true })
  public onNodeChange() {
    this.init()
  }

  public mounted() {
    this.init()
  }
}
