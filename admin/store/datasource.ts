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

  @Mutation public GET_APP_DATA_SOURCE(data: DataSource[]) { this.dataSource = data }

  @Action({ rawError: true, commit: 'GET_APP_DATA_SOURCE' })
  public getAppDataSource(id) {
    const res = service.editor.getPageDetails(id)
    return res.data.data
  }
}

export default DataSourceModule
