import { Component, Prop, Vue } from "nuxt-property-decorator"

@Component
export default class RowMixin extends Vue {
  @Prop([Object]) row
}
