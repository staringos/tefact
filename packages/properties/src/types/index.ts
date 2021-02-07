export interface IPropertiesRowParams {
  title: string;
  path: string;
}

export interface IPropertiesRow {
  type: string;
  params: IPropertiesRowParams
}

export interface IPropertiesComponents {
  type: string;
  params: {
    title?: string;
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
