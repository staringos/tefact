import { Vue, Component, Prop, Watch } from 'vue-property-decorator'
import { IFormNode } from "../types"

@Component
export default class FieldMixin extends Vue {
  @Prop() value!: any
  @Prop() node!: IFormNode
  tmpInput = ""

  @Watch('value', { immediate: true })
  handleValueChange() {
    this.tmpInput = this.value || (this as any).originDate
  }

  @Watch('tmpInput', { immediate: true })
  handleTmpInputChange() {
    this.$emit('input', this.tmpInput)
  }
}
