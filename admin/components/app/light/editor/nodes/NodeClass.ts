import { Vue, Component, Prop } from 'nuxt-property-decorator';
import { BaseNodeModel, ImageNodeModel, TableNodeModel, TextNodeModel } from '~/utils/entities/editor/node'

@Component
export default class NodeClass extends Vue {
  @Prop() public sectionId!: string
  @Prop() public node!: BaseNodeModel | TextNodeModel | ImageNodeModel | TableNodeModel
  @Prop() public preview!: boolean
}
