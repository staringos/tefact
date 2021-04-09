import { Component, Prop, Watch } from "vue-property-decorator"
import get from "lodash/get"
import set from "lodash/set"
import cloneDeep from "lodash/cloneDeep"
import { BaseNodeStyle, DefaultNodeData, IBaseNode, BaseView } from "@tefact/core"
import { IPropertiesRow } from "../types"

@Component
export default class RowMixin extends BaseView {
  @Prop([Object]) row?: IPropertiesRow
  @Prop([String]) title?: string
  @Prop([String]) path!: string
  @Prop() public node!: IBaseNode
  @Prop() public nodeType!: string
  @Prop() public isDirectModify?: boolean
  // @editor.Action public modifyNode

  public tmpText = ""
  public tmpNode: IBaseNode | null = null

  // get style() {
  //   if (this.tmpNode)
  //     return this.tmpNode.style
  //   return null
  // }

  get currentData() {
    return get(this.tmpNode, this.path)
  }

  @Watch('node', { deep: true, immediate: true })
  public onNodeChange() {
    this.init()
  }

  @Watch("tmpNode", { deep: true, immediate: true })
  public handleTmpNodeChange() {
    this.tmpText = get(this.tmpNode, this.path)
  }

  // public handleStyleChange(key: string, value: any) {
  //   if (!this.style) return
  //   (this.style as any)[key] = value
  //   this.handleSave()
  // }

  public handleSave() {
    if (this.isDirectModify)
      return this.$emit("modify", this.tmpNode)
    this.engine.updateNode(this.tmpNode)
  }

  public init() {
    if (!this.node) return
    const tmpNode = cloneDeep(this.node)
    if (!tmpNode && DefaultNodeData[this.nodeType])
      this.tmpNode = DefaultNodeData[this.nodeType].config

    if (tmpNode && !tmpNode.style)
      tmpNode.style = BaseNodeStyle

    this.tmpNode = tmpNode
  }

  handleChange(e: Event) {
    if (!this.tmpNode) return
    set(this.tmpNode, this.path, e)
    this.handleSave()
  }

  public mounted() {
    this.init()
  }
}
