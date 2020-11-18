import { Route } from './vue'

export interface LightAppParams {}

export interface Application {
  id: string;
  key: string;
  path?: string;
  routes?: Route[];
  name?: string;
  type?: string;
  title?: string;
  is_install?: number;
  description?: string;
  icon?: string;
  api_route?: string;
  admin_route?: string;
  sort?: number;
  images: string[];
  application_category?: ApplicationCategory;
  version?: string;
  install_number?: number;
  create_time?: number;
  menus: Menu[] | null | [];
}

export interface ApplicationCategory {
  name: string;
}

interface Menu {
  name: string;
  path: string;
  icon: string;
}
