import { BaseNodeModel } from "~/utils/entities/editor/node"

export interface PageSectionModel {
  title?: string
  section_type: string
  page_id: string
  nodes: BaseNodeModel[]
}

export interface PageModel {
  title: string
  direction: string
  type: string
  page_section: PageSectionModel[]
}
