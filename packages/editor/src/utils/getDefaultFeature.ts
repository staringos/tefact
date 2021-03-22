import { getDefault as getPageDefault } from "@tefact/feature-page";
import { getDefault as getFormDefault } from "@tefact/feature-form";

export default function getDefaultFeature(displayType: string) {
  const res = getPageDefault(displayType);
  if (res) return res;
  return getFormDefault(displayType);
}
