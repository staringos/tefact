import TextNode from './TextNode.vue'
import ImageNode from './ImageNode.vue'
import TableNode from './TableNode.vue'
import ButtonNode from './ButtonNode.vue'
import CardNode from './CardNode.vue'
import CarouselNode from './CarouselNode.vue'
import BrowserNode from './BrowserNode.vue'
import FormNode from './FormNode.vue'
import ShapeNode from './ShapeNode.vue'
import SectionNode from './SectionNode.vue'
import TabBarNode from './TabBarNode.vue'
import HeaderBarNode from './HeaderBarNode.vue'
import { PageProperties } from "../config"
import { IProperties } from "@tefact/properties"
import { NodeConfig } from "@tefact/core"

const nodes = {
  SectionNode,
  TextNode,
  ImageNode,
  TableNode,
  ButtonNode,
  CardNode,
  CarouselNode,
  BrowserNode,
  ShapeNode,
  TabBarNode,
  HeaderBarNode,
  FormNode
} as Record<string, any>

export default nodes

const PROPERTIES = { ...PageProperties.PROPERTIES }  as Record<string, IProperties>
const NODES = {} as Record<string, NodeConfig>;

Object.keys(nodes).forEach((key: string) => {
  const node = nodes[key];
  if (!node) return;
  if (node.PROPERTIES) PROPERTIES[key] = node.PROPERTIES
  if (node.NODE) NODES[key] = node.NODE
})

export {
  PROPERTIES,
  NODES
}
