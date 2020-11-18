import { Vue, Component, Prop, Watch } from 'nuxt-property-decorator'
import cloneDeep from 'lodash/cloneDeep'
import { BaseNodeModel, EditorNodeData } from '~/utils/entities/editor/node'
import { BaseNodeStyle, NodeDefaultData } from '~/utils/constants/Editor'

@Component
export default class ResoluMixin extends Vue {
  @Prop() public node!: BaseNodeModel<EditorNodeData>
  @Prop() public nodeType!: string

  public tmpNode!: BaseNodeModel<EditorNodeData>

  public init() {
    if (!this.node) return
    const tmpNode = cloneDeep(this.node)
    if (!tmpNode.config)
      tmpNode.config = NodeDefaultData[this.nodeType].config

    if (!tmpNode.config.style)
      tmpNode.config.style = BaseNodeStyle

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
