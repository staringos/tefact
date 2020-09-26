declare module '*.vue' {
  import Vue from 'vue'
  // noinspection JSDuplicatedDeclaration
  export default Vue
}

declare module '@/src/pages/**/*' {
  import Vue from 'vue'
  // noinspection JSDuplicatedDeclaration
  export default Vue
}

declare module '@/src/components/**/*' {
  import Vue from 'vue'
  // noinspection JSDuplicatedDeclaration
  export default Vue
}

interface MyWindow extends Window {
  WxLogin(): void;
}

declare let window: MyWindow

declare module '@nuxt/utils'
