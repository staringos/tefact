import { DEFAULT as PAGE_DEFAULT } from "@tefact/feature-page";
import { DEFAULT as FORM_DEFAULT } from "@tefact/feature-form";

export default function getDefaultFeature(type: string) {
  return type === "form" ? FORM_DEFAULT : PAGE_DEFAULT
}
