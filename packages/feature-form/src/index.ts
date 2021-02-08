import FormModules from "./Form.vue";
import { NodeConfig } from "@tefact/core";
import { FormProperties } from "./config"
import { IProperties } from "@tefact/properties"

export * from "./constants";

export interface IForm {};
export const PROPERTIES = {
  FormPage: FormProperties.PROPERTIES
} as Record<string, IProperties>;

export const NodeList = {} as Record<string, NodeConfig>;
export default FormModules;

