import { BaseNodeModel } from "~/utils/entities/editor/node"

export interface PageSectionModel {
  id: string;
  title?: string;
  section_type: string;
  page_id: string;
  nodes: BaseNodeModel[];
}

export interface PageModel {
  id: string;
  key: string;
  title: string;
  direction: string;
  type: number;
  unique_id: string;
  application_id: string;
  page_section: PageSectionModel[];
}
