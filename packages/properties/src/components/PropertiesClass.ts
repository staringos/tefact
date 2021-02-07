import { Component, Prop } from 'vue-property-decorator'
import { BaseView, IBaseNode } from '@tefact/core'

@Component
export default class PropertiesClass extends BaseView {
  @Prop(Boolean) public isDirectModify?: boolean

  get style() {
    if (this.tmpNode)
      return this.tmpNode.style
    return null
  }

  public tmpNode: IBaseNode | null = null

  public handleStyleChange(key: string, value: string | number) {
    if (!this.style || !this.tmpNode) return
    (this.tmpNode.style as any)[key] = value
    this.handleSave()
  }

  public handleSave() {
    if (!this.tmpNode) return;
    if (this.isDirectModify)
      return this.$emit("modify", this.tmpNode)
    this.engine.updateConfig(this.tmpNode)
  }
}
