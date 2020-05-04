import { Component, Prop, Vue } from 'nuxt-property-decorator';
import { BaseNodeModel } from '~/utils/entities/editor/node';

@Component
export default class ResoluBase extends Vue {
  public tmpNode!: BaseNodeModel
}
