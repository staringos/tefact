import InputNode from './InputNode.vue'
import NumberNode from './NumberNode.vue'
import DateNode from './DateNode.vue'
import RadioNode from './RadioNode.vue'
import TextAreaNode from './TextAreaNode.vue'
import SelectNode from './SelectNode.vue'
import CheckboxNode from './CheckboxNode.vue'
import PhoneNode from './PhoneNode.vue'
import StarNode from './StarNode.vue'
import MoneyNode from './MoneyNode.vue'
import ImageNode from './ImageNode.vue'
import FormTextNode from './FormTextNode.vue'
import FormImageNode from './FormImageNode.vue'
import { FormProperties } from "../config"

const nodes = {
  InputNode,
  NumberNode,
  DateNode,
  RadioNode,
  TextAreaNode,
  CheckboxNode,
  PhoneNode,
  StarNode,
  MoneyNode,
  ImageNode,
  FormTextNode,
  FormImageNode,
  SelectNode
} as Record<string, any>;

export default nodes

const PROPERTIES = { FormPage: FormProperties.PROPERTIES } as Record<string, any>;
const NODES = {} as Record<string, any>;

Object.keys(nodes).forEach((key) => {
  const node = nodes[key];

  if (node.PROPERTIES) PROPERTIES[key] = node.PROPERTIES
  if (node.NODE) NODES[key] = node.NODE
})

export {
  PROPERTIES,
  NODES
}
