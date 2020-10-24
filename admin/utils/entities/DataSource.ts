import { cloneDeep } from "lodash";

enum DataSourceType {
  mysql = 'mysql',
  mongodb = 'mongodb',
  postgresql = 'postgresql',
  clickhouse = 'clickhouse',
}

enum DataSourceStatus {
  connected = 'connected',
  error = 'error',
  lack = 'lack',
  default = 'default'
}

export interface DataSource {
  id?: string;
  name: string;
  type: DataSourceType;
  status: DataSourceStatus;
  org_id: string;

  description?: string;
  host?: string;
  port?: string;
  username?: string;
  password?: string;
  default_db?: string;

  create_user_id: string;
}

export const DefaultDataSource: DataSource = {
  create_user_id: "",
  name: "",
  org_id: "",
  status: DataSourceStatus.default,
  type: DataSourceType.mysql
}



export const getDefaultDataSource = (): DataSource => cloneDeep(DefaultDataSource)
