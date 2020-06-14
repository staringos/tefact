declare module "*.vue" {
  import Vue from "vue"
  export default Vue
}

interface MyWindow extends Window {
  WxLogin(): void;
}

declare var window: MyWindow

declare module '@nuxt/utils'
