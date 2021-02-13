import { IBaseNode, ITarget, ITargetConfig } from "@tefact/core"

export interface FormRulesModel {
  required: boolean;
  message: string;
  itemType?: 'style' | 'field';
  trigger: 'blur' | 'click';
}

export interface FormButton {
  id?: string;
  label: string;
  type: 'submit' | 'cancel' | 'link' | 'clear';
  styleType: 'primary' | 'default' | 'warning' | 'danger' | 'success';
  size: 'small' | 'mini' | 'medium';
}

export interface IFormNodeAttr {
  type: string;
  key: string | number;
  default: string | number;
  notNull: boolean;
  label: string;

  formRules?: Array<FormRulesModel>;
  desc?: string;
  children?: Array<IFormNode>;
  link?: string;
  dateType?: string;
  placeholder?: string;
  list?: Array<any>;
}

export type IFormNode = IBaseNode & IFormNodeAttr

export type IFormConfig = {
  defaultForm?: any;
  labelWidth?: number;
  buttons?: FormButton[];
  children: Array<IFormNode>;
} & ITargetConfig

export type IFormTarget = ITarget & {
  config: IFormConfig
}
