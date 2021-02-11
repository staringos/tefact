import { Vue, Component } from "vue-property-decorator";
import Engine from "./engine";
import { DEFAULT_SETTING } from "./constants"

@Component
export class BaseView extends Vue {
  engine: Engine = Vue.observable(Engine.instance());

  get activeNodeType() { return this.activatedNode?.type }
  get activeNodeId() { return this.engine.activeNodeIds?.[0] }
  get activatedNode() { return this.engine.activatedNode; }
  get currentTarget() { return this.engine.target; }
  get featureType() { return this.engine.featureType; }
  get isForm() {
    return this.engine.isForm;
  }
  get setting() {
    return this.engine.setting;
  }

  getFormList() {
    return this.setting.formList;
  }
}

export default Engine;
