import { Vue } from "vue-property-decorator";
import Engine from "./engine";

export class BaseView extends Vue {
  engine: Engine = Vue.observable(Engine.instance());
}

export default Engine;
