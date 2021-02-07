declare module "*.vue" {
  import Vue from "vue";
  import { IEngine } from '@tefact/common'
  export default class extends Vue {
    $engine: IEngine
  };
}

declare module 'vue/types/vue' {
  interface Vue {
    /** Used to show feedback after an activity. The difference with Notification is that the latter is often used to show a system level passive notification. */
    $message: ElMessage
  }
}

declare module "*.json" {
  const value: any;
  export default value;
}
