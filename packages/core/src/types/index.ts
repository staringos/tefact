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
  application_id?: string;
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
  slots?: Record<string, IBaseNode>;
}

export type POS = { x: number; y: number };

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
  slots?: Record<string, IBaseNode>;
  slotName?: string;
}

export interface IDataSet {
  id: string;
  name: string;
  union: string;
  type: 'custom' | 'datasource';
  bind_type: 'app' | 'target';
  data_type: 'string' | 'number' | 'array' | 'object';
  datasource_id?: string;
  data_table_id?: string;
  application_id?: string;
  target_id?: string;
  data: any;
}

export type DeviceType = "pc" | "mobile";

type TargetHandler = (id: string) => Promise<ITarget> | null;

export interface IFile {
    create_time: number;
    deletable:  boolean;
    id: string;
    name: string;
    path: string;
    size: number;
    tag: null
    type: number;
    update_time: number;
    user_id: string;
}

export interface ISetting {
  app?: {
    id?: string;
    type: string
  };
  device: DeviceType;
  uploadUrl: string;
  grid?: boolean;
  customHeader?: Record<string, any>;
  formList?: Array<ITarget>;
  targetList?: Array<ITarget>;
  datasetList?: Array<IDataSet>;
  theme: "default";
  i18n: "zh-CN";
  getTargetByIdHandler?: TargetHandler;
  onFormDataSubmit?: (data: any) => Promise<boolean>;

  // target
  onShare: any;
  onPublish?: any;
  onGetTargetList?: () => Promise<Array<ITarget>>;

  // file
  onGetFileList?: (page: IPagination) => Promise<Array<IFile>>;
  onDeleteFile?: (id: string) => boolean;

  // data set
  onGetDataSet?: () => Promise<Array<IDataSet>>;
  onModifyDataSet?: (dataSet: IDataSet) => Promise<boolean>;
  onDeleteDataSet?: (id: String) => Promise<boolean>;

  // widget
  onGetWidgetList?: () => Promise<Array<IWidget>>;
  onDeleteWidget?: (id: string) => Promise<boolean>;
  onAddWidget?: (widget: IWidget) => Promise<boolean>;
}

export interface IWidget {
  name: string;
  org_id?: string;
  head_image?: string;
  from_target_id?: string;
  from_node_id?: string;
  app_id?: string;
  create_user_id?: string;
  config: IBaseNode;
}

export interface IPagination {
  pageNum: number;
  pageSize: number;
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
