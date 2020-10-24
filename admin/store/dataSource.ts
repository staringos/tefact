import { Action, Module, Mutation, VuexModule } from "~/node_modules/vuex-module-decorators"
import { service } from "~/utils"
import { DataSource } from "~/services/common/entities/datasource"

@Module({
  name: 'dataSource',
  stateFactory: true,
  namespaced: true,
})
class DataSourceModule extends VuexModule {
  dataSource: DataSource[] = []

  get dataSourceGetter() {
    return this.dataSource
  }

  @Mutation public GET_APP_DATA_SOURCE(data: DataSource[]) { this.dataSource = data }

  @Action({ rawError: true, commit: 'GET_APP_DATA_SOURCE' })
  public getAppDataSource(id) {
    const res = service.editor.getPageDetails(id)
    return res.data.data
  }

  @Action({ rawError: true, commit: 'GET_APP_DATA_SOURCE' })
  public async getDataSourceList(orgId) {
    const res = await service.dataSource.getDataSourceList(orgId)
    return res.data.data
  }

  @Action({ rawError: true })
  public async addDataSource(data) {
    const res = await service.dataSource.addDataSource(data)
    if (res.data.code === 200) {
      return this.getDataSourceList(data.org_id)
    }
  }

  @Action({ rawError: true })
  public async modifyDataSource(id, data) {
    const res = await service.dataSource.modifyDataSource(id,data)
    if (res.data.code === 200) {
      return this.getDataSourceList(data.org_id)
    }
  }

  @Action({ rawError: true })
  public async deleteDataSource(id, orgId) {
    const res = await service.dataSource.deleteDataSource(id)
    if (res.data.code === 200) {
      return this.getDataSourceList(orgId)
    }
  }

  @Action({ rawError: true })
  public async testConnect(data) {
    return service.dataSource.testConnect(data)
  }
}

export default DataSourceModule
