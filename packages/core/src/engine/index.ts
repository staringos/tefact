import { Vue } from "vue-property-decorator";
import Engine from "./engine";
import { DEFAULT_SETTING } from "./constants"

export class BaseView extends Vue {
  engine: Engine = Vue.observable(Engine.instance());

  get activeNodeType() { return this.activeNode?.type }
  get activeNodeId() { return this.engine.activeNodeIds?.[0] }
  get activeNode() { return this.engine.activeNode; }
  get currentTarget() { return this.engine.target; }
  get featureType() { return this.engine.featureType; }
  get isForm() { return this.engine.isForm; }
  get setting() { return this.engine.setting || DEFAULT_SETTING; }

  getFormList() {
    return this.setting.formList;
  }
}

export default Engine;
