import { Vue, Component, Prop, Watch } from 'vue-property-decorator'
import cloneDeep from 'lodash/cloneDeep'
import isEqual from 'lodash/isEqual'
import { BaseNodeStyle, BaseView, DefaultNodeData, IBaseNode } from '@tefact/core'

@Component
export default class PropertiesMixin extends BaseView {
  @Prop() public node!: IBaseNode
  @Prop() public nodeType!: string
  @Prop(Boolean) public isDirectModify?: boolean

  public tmpNode: IBaseNode | undefined

  public init() {
    if (!this.node || isEqual(this.node, this.tmpNode)) return
    let tmpNode = Vue.observable(cloneDeep(this.node)) as IBaseNode
    if (!tmpNode && DefaultNodeData[this.featureType])
      tmpNode = DefaultNodeData[this.featureType] as IBaseNode;

    if (!(tmpNode as any).style)
      tmpNode.style = BaseNodeStyle;

    this.tmpNode = tmpNode
  }

  @Watch('node', { deep: true, immediate: true })
  public onNodeChange() {
    this.init()
  }

  get style() {
    if (this.tmpNode)
      return this.tmpNode.style
    return null
  }

  public handleStyleChange(key: string, value: string | number) {
    if (!this.tmpNode) return;
    Vue.set(this.tmpNode.style, key, value);
    this.$nextTick(() => {
      this.handleSave();
    });
  }

  public handleSave() {
    if (!this.tmpNode) return;
    if (this.isDirectModify)
      return this.$emit("modify", this.tmpNode)

    this.$nextTick(() => {
      this.tmpNode && this.engine.updateNode(this.tmpNode)
    })
  }


  public beforeMounted() {
    this.init()
  }
}
