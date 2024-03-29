export interface ISelectItem {
  value: string;
  label: string;
}

export interface IPropertiesRowParams {
  title: string;
  path: string;
  targetFeatureType?: string;
  selectOptions?: Array<ISelectItem>
}

export interface IPropertiesRow {
  type: string;
  require?: boolean;
  condition?: (cur: any) => boolean;
  params: IPropertiesRowParams
}

export interface IPropertiesComponents {
  type: string;
  params: {
    title?: string;
    path?: string;
    rows?: Array<IPropertiesRow>
  }
}

export interface IPropertiesTab {
  title: string;
  components: Array<IPropertiesComponents>;
}

export interface IProperties {
  title: string;
  hasTab: boolean;
  tabs: Array<IPropertiesTab>
}
