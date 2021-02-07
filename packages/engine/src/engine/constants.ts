import { ISetting } from "@tefact/common";

export const DEFAULT_SETTING: ISetting = {
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
