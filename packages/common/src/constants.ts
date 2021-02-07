import { IBaseNode, INodeData, INodeStyle, ITarget } from './index'

export const DefaultTarget: ITarget = {
  id: "",
  title: "这是一个新页面",
  feature: "page",
  config: {
    style: {} as INodeStyle,
    data: {
      target: ""
    },
    children: [] as IBaseNode[]
  },
}
