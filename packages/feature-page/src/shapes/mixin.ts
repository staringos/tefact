import { Vue, Component, Prop } from 'vue-property-decorator'
import type { IBaseNode } from "@tefact/core"

@Component
export default class ShapeMixin extends Vue {
  @Prop() node!: IBaseNode

  get style() {
    return this.node?.style
  }

  getStyle() {
    if (!this.node) return
    const style = this.node.style
    return `
      width: 100%;
      height: 100%;
      fill: ${style['background-color']};
      stroke-width: ${style['border-width']};
      stroke: ${style['border-color']};
    `
  }
}
