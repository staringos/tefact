import PageModules from "./Page.vue";
import { NodeConfig } from "@tefact/core";
import { PageProperties } from "./config"
import { IProperties } from "@tefact/properties"

export const PROPERTIES = {
  ...PageProperties.PROPERTIES
} as Record<string, IProperties>;
export const NodeList = {} as Record<string, NodeConfig>;
export default PageModules;
