import { EditorNodeStyle } from "~/utils/entities/editor/node"

export interface FormModel {
  id: string;
  title: string;
  description?: string;
  config?: FormConfigModel;
  validations?: FormValidation[];
}

export interface FormConfigModel {
  style: EditorNodeStyle;
  items?: FormItemModel[];
  defaultForm?: any;
}

export interface FormItemModel {
  id: string;
  style: EditorNodeStyle;
  label: string;
  key: string;
  default: any;
  type: string;
}

export interface FormValidation {
  name?: string;
}

export const DefaultFormItem: FormItemModel = {
  id: "",
  style: {} as EditorNodeStyle,
  label: '用户名',
  key: 'username',
  default: '',
  type: 'InputNode'
}

export const DefaultForm: FormModel = {
  id: "",
  title: "用户表",
  description: "string",
  config: {
    items: [{ ...DefaultFormItem }],
    style: {}
  },
  validations: []
}
