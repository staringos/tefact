export interface EditorNodeData {
}

export interface EditorNodeStyle {
  borderColor?: string
  borderWidth?: number[] | number // top right bottom left border width
  borderStyle?: string[] | string // top right bottom left border style
  bgColor?: string[] | string // top right bottom left border style
  bgImageUrl?: string
  textColor?: string
  textSize?: string
  zIndex?: number
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

export interface TextNodeData {
  text: string
}

export interface ImageNodeData {
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
