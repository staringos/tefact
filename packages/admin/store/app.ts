import { Module, VuexModule, Mutation, Action } from 'vuex-module-decorators'
import { systemStore } from '~/utils/store-accessor'
import { DIALOG_NAME } from './system'
import { OrgConfig, Application } from '@arrplat/common'
import { service } from '~/utils'

@Module({
  name: 'app',
  stateFactory: true,
  namespaced: true,
})
class AppModule extends VuexModule {
  public apps: Application[] = []
  public allApps: Application[] = []
  public orgs: OrgConfig[] = []
  public currentOrgId: string | null = null
  public currentAppId: string | null = null
  public createOrgDialogFlag = false

  @Mutation public GET_APPS(apps: Application[]) { this.apps = apps }
  @Mutation public GET_ALL_APPS(apps: Application[]) { this.allApps = apps }
  @Mutation public GET_ORGS(orgs) { this.orgs = orgs }
  @Mutation public SET_CURRENT_ORG_ID(currentOrgId) { this.currentOrgId = currentOrgId }
  @Mutation public SET_CURRENT_APP_ID(currentAppId) { this.currentAppId = currentAppId }
  @Mutation public SET_ORG_DIALOG_FLAG(orgDialogFlag) { this.createOrgDialogFlag = orgDialogFlag }

  get currentOrgIdGetter() { return this.currentOrgId }
  get orgApps() { return this.apps }
  get allAppsGetter() { return this.allApps }
  get allOrgs() { return this.orgs }
  get getCreateOrgFlag() { return this.createOrgDialogFlag }

  get currentOrg() {
    if (this.currentOrgId) {
      if (!this.orgs) return null

      const res = this.orgs.filter(org => org.id === this.currentOrgId)
      return res.length > 0 ? res[0] : this.orgs[0]
    }
    return this.orgs ? this.orgs[0] : null
  }

  get currentApp() {
    if (process.server) return null

    let current: (Application | null) = null
    this.apps && this.apps.map(plus => {
      if (plus.id === this.currentAppId) current = plus
    })
    return current
  }

  @Action({ commit: 'GET_APPS', rawError: true })
  public async removeLightApp(appId) {
    const res = await service.app.removeLightApp(appId)
    if (res.status === 200) {
      this.getAllAppsInOrg(this.currentOrgId)
      this.getAllApps(this.currentOrgId)
    }
  }

  @Action({ commit: 'GET_APPS', rawError: true })
  public async getAllAppsInOrg(orgId) {
    const res = await service.app.getAllApps(orgId, 0)
    return res.data.data
  }

  @Action({ commit: 'GET_ALL_APPS' })
  public async getAllApps(orgId) {
    const res = await service.app.getAllApps(orgId, 1)
    return res.data.data
  }


  @Action({ rawError: true })
  public async init() {
    const orgs = await this.getAllOrgs(1)
    orgs.length > 0 && await this.getAllAppsInOrg(this.currentOrg.id)
    if (orgs.length < 1) await this.setOrgDialogFlag(true)

    const path = location.href
    let currentApp = {} as any



    this.apps.map(plus => {
      if (path.indexOf(`plugins/${plus.admin_route}`) !== -1 || path.indexOf(`light/${plus.admin_route}`) !== -1)
        currentApp = plus
    })

    return currentApp.id && this.setCurrentAppId(currentApp.id)
  }

  @Action({ commit: 'GET_ORGS' })
  public async getAllOrgs(hasDetails = 1) {
    const orgList = await service.app.getAllOrgs(hasDetails)
    if (!orgList.data) return null

    const data = orgList.data.data

    if (data.length === 0)
      systemStore.setDialogVisible({ key: DIALOG_NAME.NO_ORG_DIALOG, visible: true })

    // auto select first org
    if (!this.currentOrgId && data.length > 0)
      this.setCurrentOrgId(data[0].id)

    return data
  }

  @Action({ commit: 'SET_CURRENT_ORG_ID' })
  public setCurrentOrgId(currentId) {
    return currentId
  }

  @Action({ commit: 'SET_CURRENT_APP_ID', rawError: true })
  public setCurrentAppId(currentId) {
    return currentId
  }

  @Action({ rawError: true })
  public async onOrgChanged(currentOrgId) {
    await this.setCurrentOrgId(currentOrgId)
    return await this.init()
  }

  @Action({ commit: 'SET_ORG_DIALOG_FLAG' })
  public setOrgDialogFlag(orgDialogFlag) {
    return orgDialogFlag
  }

  @Action
  public async toggleApp({ appId, orgId, isAdd }) {
    const res = await service.app[isAdd ? 'addApp' : 'removeApp'](appId, orgId)
    if (res.status === 200) {
      this.getAllAppsInOrg(orgId)
      this.getAllApps(orgId)
    }
    return res
  }

  @Action({ rawError: true })
  public async lightAppAdd(params) {
    const res = await service.app.lightAppAdd(params)
    if (res.status === 200)
      await this.getAllAppsInOrg(params.own_org_id)
  }

  @Action({ rawError: true })
  public getAppDetails(id) {
    return service.app.getAppDetails(id)
  }

  @Action({ rawError: true })
  public addMenu(data) {
    return service.app.addMenu(data)
  }

  @Action({ rawError: true })
  public addPage(data) {
    return service.app.addPage(data)
  }
}

export default AppModule
