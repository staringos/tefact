import { Vue, Component, Prop } from 'nuxt-property-decorator'
import _ from 'lodash'
import { BaseNodeModel } from '~/utils/entities/editor/node'
import { NodeDefaultData } from '~/utils/constants/Editor'

@Component
export default class ResoluMixin extends Vue {
  @Prop() public node!: BaseNodeModel
  @Prop() public nodeType!: string

  public tmpNode!: BaseNodeModel

  public mounted() {
    const tmpNode = _.cloneDeep(this.node)
    if (!tmpNode.config) {
      tmpNode.config = NodeDefaultData[this.nodeType].config
    }

    this.tmpNode = tmpNode
  }
}
