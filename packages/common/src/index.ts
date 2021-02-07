import * as CSS from "csstype";

export type TargetFeatureType = "page" | "form";

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
  featureType: TargetFeatureType;
  config: ITargetConfig;
}

export interface INodeStyle extends CSS.PropertiesHyphen<string | number, number> {}

export interface INodeData {
  target: any;
}

export interface ITargetConfig {
  style: INodeStyle;
  data: INodeData;
  children: IBaseNode[];
}

export interface IPos {
  x: number;
  y: number;
  w: number;
  h: number;
}

export interface IBaseNode {
  id: string;
  type: string;
  pos: IPos;
  style: INodeStyle;
  data?: INodeData;
  children?: IBaseNode[];
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

export type NodeListConfig = {
  title: string | null;
  list: Record<string, NodeConfig>
}

export type NodeConfig = {
  title: string
  icon: string
  type: string
  nodeData: IBaseNode
}
