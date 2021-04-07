import { FormButton, FormRulesModel, IFormNode } from "./types"
import { INodeStyle } from "@tefact/core"
import DEFAULT_JSON from "./data/DEFAULT.json"

export const DefaultForm = {}

export const DefaultMainButton: FormButton = {
  id: '',
  label: '确定',
  type: 'submit',
  styleType: 'primary',
  size: 'medium'
}

export const DefaultSecondButton: FormButton = {
  id: '',
  label: '清除',
  type: 'clear',
  styleType: 'default',
  size: 'medium'
}

export const DefaultFormItem: IFormNode = {
  id: "DEFAULT_FORM_ITEM_123",
  key: 'username',
  type: 'InputNode',
  style: {} as INodeStyle,
  pos: {
    h: 0,
    w: "100%",
    x: 0,
    y: 0
  },
  data: {},
  label: '用户名',
  default: '',
  desc: '可以是手机号或邮箱',
  placeholder: '请输入内容',
  notNull: false,
  formRules: [] as Array<FormRulesModel>,
}

export const DEFAULT = DEFAULT_JSON;
//   {
//   "title": "这是一个新表单",
//   "featureType": "form",
//   config: {
//     children: [{ ...DefaultFormItem }],
//     style: {},
//     labelWidth: 100,
//     viewMode: 'fixed',
//     buttons: [
//       { ...DefaultMainButton },
//       { ...DefaultSecondButton },
//     ]
//   }
// }

export const getDefault = (displayType: string) => {
  if (displayType === "form") {
    return DEFAULT;
  }
}
