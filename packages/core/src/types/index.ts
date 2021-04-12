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
  share?: ShareInfo; // the target share information
}

export interface INodeStyle extends CSS.PropertiesHyphen<string | number, number> {}

export interface INodeData {
  target?: any;
}

export type FreeNodeData = Record<string, any>;

export interface ITargetConfig {
  style: INodeStyle;
  pos?: IPos;
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
  onFormDataSubmit?: (data: any) => Promise<boolean>;
  getTargetByIdHandler?: TargetHandler;
  onShare: any;
}

export interface ShareInfo {
  key: string;
  password: string;
  id: string;
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
  list: Array<NodeConfig>;
  // list: Record<string, NodeConfig>;
  categories?: Array<string>;
  classifiedList?: Record<string, Record<string, NodeConfig>>;
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
