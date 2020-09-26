export interface DataSource {
  id: string;
  name: string;
  path: string;
  type: DataSourceType;
}

export interface DataBaseConnect {

}

export interface DataFile {

}

export interface DataTable {

}

enum DataSourceType {
  mysql, excel
}

