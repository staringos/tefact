import { Component, Prop, Watch } from 'vue-property-decorator'
import cloneDeep from 'lodash/cloneDeep'
import { BaseNodeStyle, BaseView, DefaultNodeData, IBaseNode } from '@tefact/core'

@Component
export default class PropertiesMixin extends BaseView {
  @Prop() public node!: IBaseNode
  @Prop() public nodeType!: string
  @Prop(Boolean) public isDirectModify?: boolean

  public tmpNode: IBaseNode | undefined

  public init() {
    if (!this.node) return
    let tmpNode = cloneDeep(this.node) as IBaseNode
    if (!tmpNode && DefaultNodeData[this.featureType])
      tmpNode = DefaultNodeData[this.featureType] as IBaseNode;

    if (!(tmpNode as any).style)
      tmpNode.style = BaseNodeStyle;

    this.tmpNode = tmpNode
  }

  @Watch('node', { deep: true, immediate: true })
  public onNodeChange() {
    console.log("node change:", this.node);
    this.init()
  }

  get style() {
    if (this.tmpNode)
      return this.tmpNode.style
    return null
  }

  public handleStyleChange(key: string, value: string | number) {
    if (!this.style || !this.tmpNode) return
    (this.tmpNode.style as any)[key] = value
    this.handleSave()
  }

  public handleSave() {
    console.log("handleSave:", this.tmpNode)
    if (!this.tmpNode) return;
    if (this.isDirectModify)
      return this.$emit("modify", this.tmpNode)

    this.$nextTick(() => {
      console.log("(((((((((( before:", this.tmpNode)
      this.engine.updateNode(this.tmpNode)
    })
  }


  public beforeMounted() {
    this.init()
  }
}
