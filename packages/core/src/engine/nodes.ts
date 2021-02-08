import { IBaseNode, INodeStyle } from "../types";
import isNumber from "lodash/isNumber";
import cloneDeep from "lodash/cloneDeep";

export const BaseNodeStyle: INodeStyle = {
  'border-width': 0,
  'border-radius': 0,
  'font-size': 12,
  'color': '#333'
}

export const DefaultBaseNode: IBaseNode = {
  id: "",
  type: "TextNode",
  pos: {
    x: 30,
    y: 30,
    w: 120,
    h: 80,
  },
  style: { ...BaseNodeStyle },
}

export const getBaseNode = (width?: number, height?: number, additionConfig?: any): IBaseNode => {
  let res = cloneDeep(DefaultBaseNode);
  if (isNumber(width)) res.pos.w = width
  if (isNumber(height)) res.pos.h = height
  if (additionConfig) res = { ...res, ...additionConfig }
  return res;
}
