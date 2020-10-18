import { ButtonNativeType, ButtonType } from "element-ui/types/button";
import { ElementUIComponentSize } from "element-ui/types/component"

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

export interface BaseNodeModel<T extends EditorNodeData> {
  config: EditorNodeConfig;
  data: T;
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

export declare interface ElButton {
  /** Button size */
  size?: ElementUIComponentSize;

  /** Button type */
  type?: ButtonType;

  /** Determine whether it's a plain button */
  plain?: boolean;

  /** Determine whether it's a round button */
  round?: boolean;

  /** Determine whether it's loading */
  loading?: boolean;

  /** Disable the button */
  disabled?: boolean;

  /** Button icon, accepts an icon name of Element icon component */
  icon?: string;

  /** Same as native button's autofocus */
  autofocus?: boolean;

  /** Same as native button's type */
  nativeType?: ButtonNativeType;
}

export type BaseButtonNodeData = ElButton & EditorNodeData

export interface ButtonNodeData extends BaseButtonNodeData {
  text?: string;
  link?: string;
}

export type ButtonNodeModel = BaseNodeModel<ButtonNodeData>
export type TextNodeModel = BaseNodeModel<TextNodeData>
export type ImageNodeModel = BaseNodeModel<ImageNodeData>
export type HTMLCodeNodeModel = BaseNodeModel<ImageNodeData>
export type TableNodeModel = BaseNodeModel<TableNodeData>
