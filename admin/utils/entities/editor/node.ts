
export interface EditorNodeData {
  data?: any;
}

export interface EditorNodeStyle {
  'border-color'?: string;
  'border-width'?: number[] | number; // top right bottom left border width
  'border-style'?: string[] | string; // top right bottom left border style
  'background-color'?: string[] | string; // top right bottom left border style
  'background-image'?: string;
  'text-color'?: string;
  'text-size'?: string;
  'z-index'?: number;
}

export interface EditorNodeConfig {
  x: number;
  y: number;
  w: number;
  h: number;
  style: EditorNodeStyle;
}

enum NodeType {
  Text = "text",
  Image = "image",
  Table = "table",
  Html = "html-code",
  Layer = "layer",
  List = "list",
  Button = "button",
}

export interface BaseNodeModel {
  config: EditorNodeConfig;
  data: EditorNodeData;
  type: NodeType;
  id?: string;
}

export interface TextNodeData extends EditorNodeData {
  text: string;
}

export interface ImageNodeData extends EditorNodeData {
  url: string | null;
  title?: string;
}

export interface SearchCondition {
  field: string;
  operation: string;
  value: string | string[] | number | number[];
}

export interface OrderCondition {
  field: string;
  type: 'asc' | 'desc';
}

export interface PageCondition {
  pageNumber: number;
  total: number;
  pageSize: number;
}

export interface DataField {
  key: string;
}

export interface DataTable {
  type: 'table' | 'view';
  fields: DataField[];
}

export interface DataSource {
  type: 'mysql' | 'csv' | 'excel';
  url: string;
  username?: string;
  password?: string;
  tables: DataTable[];
}

export interface TableNodeData extends EditorNodeData {
  searchCondition?: SearchCondition[];
  orderCondition?: OrderCondition[];
  pageCondition?: PageCondition;
  dataSource?: DataSource;
  title?: string;
  dataSourceId?: string | null;
  entityId?: string | null;
}

export interface TextNodeModel extends BaseNodeModel {
  data: TextNodeData;
}

export interface ImageNodeModel extends BaseNodeModel {
  data: ImageNodeData;
}

export interface HTMLCodeNodeModel extends BaseNodeModel {
  data: ImageNodeData;
}

export interface TableNodeModel extends BaseNodeModel {
  data: TableNodeData;
}
