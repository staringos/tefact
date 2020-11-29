import { Vue, Component, Prop, namespace } from "nuxt-property-decorator";
import { BaseNodeModel, EditorNodeData } from '~/utils/entities/editor/node';
const editor = namespace('editor')

@Component
export default class ResoluClass extends Vue {
  @Prop() public nodeType
  @Prop() public isDirectModify
  @editor.Action public modifyNode

  get style() {
    if (this.tmpNode)
      return this.tmpNode.config.style
    return null
  }

  public tmpNode: BaseNodeModel<EditorNodeData> | null = null

  public handleStyleChange(key, value) {
    if (!this.style) return
    this.style[key] = value
    this.handleSave()
  }

  public handleSave() {
    if (this.nodeType === 'page') return
    if (this.nodeType === 'section') return

    if (this.isDirectModify)
      return this.$emit("modify", this.tmpNode)
    this.modifyNode({ sectionId: null, node: this.tmpNode })
  }
}
