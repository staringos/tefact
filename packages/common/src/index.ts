export type TargetCompileType = "page" | "form";

export const EVENT = {
  ADD: "add",
  UPDATE: "update",
  UPDATE_CONFIG: "update_config",
  SHARE: "share",
  SAVE: "save"
}

export interface ITarget {
  id: string;
  title: string;
  feature: TargetCompileType;
  config: ITargetConfig;
}

export interface INodeStyle extends CSSStyleDeclaration {
  h: number;
  w: number;
}

export interface INodeData {
  target: any;
}

export interface ITargetConfig {
  style: INodeStyle;
  data: INodeData;
  children: IBaseNode[];
}

export interface IBaseNode {
  id: string;
  type: string;
  style: INodeStyle;
  data: INodeData;
  children: IBaseNode[];
}

export type DeviceType = "pc" | "mobile";

export interface ISetting {
  device: DeviceType;
  theme: "default";
  i18n: "zh-CN";
}

export interface IEngine {
  target?: ITarget;
  setting?: ISetting;

  add(config: IBaseNode): void;
  update(path: string, value: any): void;
  updateConfig(config: IBaseNode): void;
  save(config: IBaseNode): void;
  share(config: IBaseNode): void;
}

/* class decorator */
export function StaticImplements<T>() {
  return <U extends T>(constructor: U) => {constructor};
}
