import { Route } from './vue'

export interface PluginOptions extends PlusConfig {
  path?: string;
  routes?: Route[];
}

export interface ArrplusConfig {
  plusDir?: string;
  routeNameSplitter?: string;
  dir?: {
    pages?: string;
  };
  plus: string[];
}

// @ts-ignore
export interface ArrplusOptions extends ArrplusConfig {
  plus: PluginOptions[];
}

export interface Menu {
  name: string;
  path: string;
  icon: string;
}

export interface GlobalComponent {
  name: string;
  path: string;
}

export interface PlusConfig {
  name?: string;
  title?: string;
  description?: string;
  icon?: string;
  apiRoute?: string;
  adminRoute?: string;
  sort?: number;
  globalComponents?: GlobalComponent[];
  menus: Menu[] | null | [];
}
