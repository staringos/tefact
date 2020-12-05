import { BaseNodeModel, EditorNodeData, EditorNodeStyle } from "~/utils/entities/editor/node"

export interface PageSectionModel {
  id: string;
  title?: string;
  section_type: string;
  page_id: string;
  nodes: BaseNodeModel<EditorNodeData>[];
}

export interface PageConfigModel {
  viewMode: "fixed" | "adapt";
  style: EditorNodeStyle;
}

export interface MobilePageModel {
  type: "page" | "screen";
  screen: PageSectionModel[];
  config: PageConfigModel;

}

export interface PageModel {
  id?: string;
  key?: string;
  title: string;
  direction: string;
  type?: number;
  unique_id?: string;
  application_id?: string;
  config: PageConfigModel;
  mobile?: MobilePageModel;
  page_section: PageSectionModel[];
}
