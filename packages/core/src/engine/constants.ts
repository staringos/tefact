import { ISetting } from "../types";
import { BaseNodeStyle } from "./nodes"

export const DEFAULT_SETTING: ISetting = {
  uploadUrl: "/core/upload-files/tefact-saas",
  customHeader: {},
  formList: [],
  device: "pc",
  theme: "default",
  i18n: "zh-CN",
}

export interface Share {
  page_id?: string | null;
  type: string;
  password: string | null;
}

export const DefaultShare: Share = {
  page_id: null,
  type: 'password',
  password: null
}

export const DefaultNodeData = {
  page: {
    config: {
      style: { ...BaseNodeStyle },
    },
  },
  section: {
    style: { ...BaseNodeStyle },
  }
} as Record<string, any>
