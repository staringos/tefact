import { Module, VuexModule, Action, Mutation } from 'vuex-module-decorators'
import { Application } from '~/services/common'
import { service } from '~/utils'

@Module({
  name: 'platform',
  stateFactory: true,
  namespaced: true,
})
class AppModule extends VuexModule {
  private apps: Application[] = []

  get appsGetter() { return this.apps }

  @Mutation public GET_ALL_APPS(apps) { this.apps = apps }

  @Action
  public reConfigAndRestart() {
    return service.platform.reConfigAndRestart()
  }

  @Action({ rawError: true })
  public savePlatformConfig({ key, config }) {
    return service.platform.savePlatformConfig(key, config)
  }

  @Action({ rawError: true, commit: 'GET_ALL_APPS' })
  public async getPlatformConfig() {
    const res = await service.platform.getPlatformConfig()
    const data = res.data.data
    return data.plus.plus
  }
}

export default AppModule
