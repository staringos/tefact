import { Module, VuexModule, Mutation, Action } from 'vuex-module-decorators'
import { EntityPage } from '@arrplat/common'
import { service } from '~/utils'
import { appStore } from '~/utils/store-accessor'

@Module({
  name: 'entities',
  stateFactory: true,
  namespaced: true,
})
class AppModule extends VuexModule {
  public pages: EntityPage[] = []
  public currentPage: EntityPage = null
  public modifyData: any = {}
  public modifyDialog = false

  @Mutation public GET_APPS(page: EntityPage) { this.pages.push(page) }
  @Mutation public SET_CURRENT_PAGE(page: EntityPage) { this.currentPage = page }
  @Mutation public TOGGLE_MODIFY_DIALOG({ status, data }) {
    this.modifyDialog = status

    if (status && data) this.modifyData = data
    else this.modifyData = {}
  }

  @Mutation public SET_SECTION_NEW_DATA({ sectionId, sectionData }) {
    const currentPage = { ...this.currentPage }
    currentPage.page_section.map(section => {
      if (section.id === sectionId)
        section.entity = sectionData.entity
    })
    this.currentPage = currentPage
  }

  get pagesGetter() { return this.pages }
  get currentPageGetter() { return this.currentPage }
  get modifyDataGetter() { return this.modifyData }
  get modifyDialogGetter() { return this.modifyDialog }

  @Action({ rawError: true })
  public addDataSource(data) {
    return service.entities.addDataSource(data)
  }

  @Action({ rawError: true })
  public getDataSource(appId) {
    return service.app.getDataSource(appId)
  }

  @Action({ rawError: true })
  public getEntityData({ id, searchParams, pageParams, orderParams }) {
    return service.entities.getEntityData({ id, searchParams, pageParams, orderParams })
  }

  @Action
  public getEntityConfig(key) {
    return service.entities.getEntityConfig(key)
  }

  @Action
  public deleteRowData({ id, orgId, entityId }) {
    return service.entities.deleteRowData(id, orgId, entityId)
  }

  @Action({ commit: 'SET_CURRENT_PAGE' })
  public async getPageData({ key, params, orgId }) {
    const res = await service.entities.getPage(key, params, orgId)
    const data = res.data.data
    appStore.setCurrentAppId(data.application_id)

    return data
  }

  @Action({ commit: 'SET_SECTION_NEW_DATA' })
  public async querySectionData({ pageSectionId, page, searchCondition, sort, params, orgId }) {
    const res = await service.entities.querySectionData(pageSectionId, page, searchCondition, sort, params, orgId)
    return { sectionId: pageSectionId, sectionData: res.data.data }
  }

  @Action({ rawError: true })
  public async pageModifier({ entityId, params, dataId }) {
    return service.entities.pageModifier(entityId, params, dataId)
  }

  @Action({ rawError: true })
  public async getEditorOptions({ entityId, orgId }) {
    return service.entities.getEditorOptions(entityId, orgId)
  }

  @Action({ commit: 'TOGGLE_MODIFY_DIALOG' })
  public async toggleModifyDialog({ status, data }) {
    return { status, data }
  }
}

export default AppModule
