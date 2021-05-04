import type { IBaseNode, INodeStyle, ITarget } from './index'

export const DefaultTarget: ITarget = {
  id: "",
  title: "这是一个新页面",
  featureType: "page",
  config: {
    style: {} as INodeStyle,
    data: {
      target: ""
    },
    viewMode: "adapt",
    children: [] as IBaseNode[],
    slots: {}
  },
}

export const EVENT = {
  INPUT: "input",
  ADD: "add",
  UPDATE: "update",
  UPDATE_CONFIG: "update_config",
  SHARE: "share",
  SHARE_CANCEL: "shareCancel",
  EDIT_TARGET: "editTarget",
  ADD_TARGET: "addTarget",
  SUBMIT: "submit",
  OPEN_MODIFIER: "openModifier",
  BACK: "back",
  MOVE: "move",
  SAVE: "save"
}

export const DRAGGING_TYPE = {
  MOVE: "move",
  ADD: "add",
}

export const EVENT_INSIDE = {
  SWITCH_PROPERTIES_TAB: "SWITCH_PROPERTIES_TAB",
}
