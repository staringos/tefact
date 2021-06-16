import { ISetting } from "../types";
import { BaseNodeStyle } from "./nodes";

export const DEFAULT_SETTING: ISetting = {
  app: {
    id: (new Date()).toTimeString(),
    type: "normal"
  },
  uploadUrl: "/core/upload-files/tefact-saas",
  customHeader: {},
  formList: [],
  device: "pc",
  theme: "default",
  i18n: "zh-CN",
  onShare: () => {},
}

export interface Share {
  page_id?: string | null;
  type: string;
  password: string | null;
}

export const DefaultShare: Share = {
  page_id: null,
  type: 'free',
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

export const DefaultDataset = {
  name: "",
  union: "",
  type: 'custom',
  bind_type: 'app',
  data_type: 'string',
  datasource_id: undefined,
  data_table_id: undefined,
  application_id: undefined,
  target_id: undefined,
  data: "",
}
