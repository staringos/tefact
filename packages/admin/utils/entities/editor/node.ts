
export interface EditorNodeData {
  data?: any
}

export interface EditorNodeStyle {
  'border-color'?: string
  'border-width'?: number[] | number // top right bottom left border width
  'border-style'?: string[] | string // top right bottom left border style
  'background-color'?: string[] | string // top right bottom left border style
  'background-image'?: string
  'text-color'?: string
  'text-size'?: string
  'z-index'?: number
}

export interface EditorNodeConfig {
  x: number
  y: number
  w: number
  h: number
  style: EditorNodeStyle
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
  config: EditorNodeConfig
  data: EditorNodeData
  type: NodeType
  id?: string
}

export interface TextNodeData extends EditorNodeData {
  text: string
}

export interface ImageNodeData extends EditorNodeData {
  url: string
}

export interface TextNodeModel extends BaseNodeModel {
  data: TextNodeData
}

export interface ImageNodeModel extends BaseNodeModel {
  data: ImageNodeData
}

export interface HTMLCodeNodeModel extends BaseNodeModel {
  data: ImageNodeData
}
