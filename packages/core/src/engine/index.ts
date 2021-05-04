import { Component, Vue } from "vue-property-decorator";
import Engine from "./engine";
import { ISetting } from "../types"

@Component
export class BaseView extends Vue {
  engine: Engine = Engine.instance();

  get activeNodeType() { return this.activatedNode?.type }
  get activeNodeId() {
    if (this.engine.activeNodeIds.length === 0) return null
    return this.engine.activeNodeIds?.[0]
  }
  get activatedNode() { return this.engine.activatedNode; }
  get currentTarget() { return this.engine.target; }
  get featureType() { return this.engine.featureType; }
  get isForm() {
    return this.engine.isForm;
  }
  get setting(): ISetting {
    return this.engine.setting;
  }

  get targetSlots() {
    return this.currentTarget.config.slots || {}
  }

  getFormList() {
    return this.setting.formList;
  }
}

export default Engine;
