import { Vue, Component, Prop } from 'nuxt-property-decorator';
import { BaseNodeModel, EditorNodeData } from '~/utils/entities/editor/node'

@Component
export default class NodeClass<T extends BaseNodeModel<EditorNodeData>> extends Vue {
  @Prop() public sectionId!: string
  @Prop() public node!: T
  @Prop() public preview!: boolean

  get nodeData() {
    return this.node?.data || {} as any
  }

  get config() {
    return this.node?.config || {} as any
  }
}
