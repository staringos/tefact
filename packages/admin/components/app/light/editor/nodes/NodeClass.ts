import { Vue, Component, Prop } from "nuxt-property-decorator";
import { BaseNodeModel } from '~/utils/entities/editor/node';

@Component
export default class NodeClass extends Vue {
  @Prop() public sectionId!: string
  @Prop() public node!: BaseNodeModel
  @Prop() public preview!: boolean
}
