export interface Page {
  id: string;
  name?: string;
  title?: string;
  page_section: PageSection[];
  html_content: string | null;
  section_type: string;
  head_image: string | null;
}

export interface EntityPageSection {
  id: string;
  entity_params: string;
  entityParams: string;
}
export interface EntityPage {
  page_section?: EntityPageSection;
}

export interface PageSection {
  id: string;
  name?: string;
  title?: string;
  html_content: string;
  page_section_to: PageSection;
  section_type: string;
}

export interface Entity {
  id: string;
  has_connect_org: boolean;
  tableName: string;
  "data_type": 1;
  "entity_data": [];
  entity_fields: EntityField[];
}

export interface EntityField {
  data_type: string;
  display_type: number;
  entity: string;
  exists_type: string;

  has_link: boolean;
  link_address: string;

  has_search: boolean;
  has_sort: boolean;
  id: string;
  is_primary: boolean;
  key: string;
  name: string;
  query_sql: string;
  sort: number;
  type: number;
}
