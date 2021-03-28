import * as CSS from "csstype";

export type TargetFeatureType = "page" | "form";
export type TargetDisplayType = "page" | "form" | "h5swift" | "h5page";

export interface IPosition {
  x: number;
  y: number;
}

export interface ITarget {
  id: string;
  title: string;
  direction?: "horizontal" | "vertical";
  featureType: TargetFeatureType;
  displayType?: TargetDisplayType;
  config: ITargetConfig;
}

export interface INodeStyle extends CSS.PropertiesHyphen<string | number, number> {}

export interface INodeData {
  target?: any;
}

export type FreeNodeData = Record<string, any>;

export interface ITargetConfig {
  style: INodeStyle;
  data: INodeData & FreeNodeData;
  viewMode: "adapt" | "fixed";
  children: IBaseNode[];
}

export interface IPos {
  x: number;
  y: number;
  w: number | string;
  h: number | string;
}

export type INodePos = IPos & {
  w: number;
  h: number;
}

export interface IBaseNode {
  id: string;
  type: string;
  pos: IPos;
  style: INodeStyle;
  data: FreeNodeData;
  children?: IBaseNode[];
}

export type DeviceType = "pc" | "mobile";

type TargetHandler = (id: string) => Promise<ITarget> | null;

export interface ISetting {
  device: DeviceType;
  uploadUrl: string;
  grid?: boolean;
  customHeader?: Record<string, any>;
  formList?: Array<ITarget>;
  theme: "default";
  i18n: "zh-CN";
  formDataSubmitHandler?: (data: any) => Promise<boolean>;
  getTargetByIdHandler?: TargetHandler;
  shareHandler: any;
}

export interface IEngine {
  target?: ITarget;
  setting?: ISetting;

  add(config: IBaseNode): void;
  update(path: string, value: any): void;
  updateNode(config: IBaseNode): void;
  save(config: IBaseNode): void;
  share(config: ShareDataType): any;
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

export type ShareDataType = {
  pageId: string;
  type: "free" | "password" | "login";
  pageType: "page" | "form" | "h5";
}
