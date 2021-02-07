import { BaseNodeStyle, getBaseNode } from './nodes'
import { NodeConfig } from "@/types";

function getDefaultShapeConfig(title: string, icon: string, shapeType: string, width?: number): NodeConfig {
  return {
    title,
    icon: icon,
    type: 'ShapeNode',
    nodeData: getBaseNode(width || 50, 50, { type: "ShapeNode", shapeType, style: { ...BaseNodeStyle, 'background-color': '#3181DE' }}),
  };
}

export const SHAPE_NODE_LIST = {
  RectShape: getDefaultShapeConfig('矩形', 'tf-icon-rect', 'RectShape'),
  HeartShape: getDefaultShapeConfig('心形', 'tf-icon-heart', 'HeartShape'),
  CircleShape: getDefaultShapeConfig('圆形', 'tf-icon-circle', 'CircleShape'),
  TriangleShape: getDefaultShapeConfig('三角形', 'tf-icon-triangle', 'TriangleShape'),
  LineShape: getDefaultShapeConfig('直线', 'tf-icon-line', 'LineShape', 5),
  StarShape: getDefaultShapeConfig('星形', 'tf-icon-star-fill', 'StarShape')
} as Record<string, NodeConfig>;
