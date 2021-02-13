import { FormButton, FormRulesModel, IFormNode } from "./types"
import { INodeStyle } from "@tefact/core"

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
  id: "",
  key: 'username',
  type: 'InputNode',
  style: {} as INodeStyle,
  pos: {
    h: 50,
    w: "100%",
    x: 0,
    y: 0
  },
  data: {},
  label: '用户名',
  default: '',
  desc: '',
  placeholder: '请输入内容',
  notNull: false,
  formRules: [] as Array<FormRulesModel>,
}

export const DEFAULT = {
  "title": "这是一个新表单",
  "featureType": "form",
  config: {
    children: [{ ...DefaultFormItem }],
    style: {},
    labelWidth: 100,
    viewMode: 'fixed',
    buttons: [
      { ...DefaultMainButton },
      { ...DefaultSecondButton },
    ]
  }
}
