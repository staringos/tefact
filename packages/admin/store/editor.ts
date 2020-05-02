import { Module, VuexModule, Action, Mutation } from "vuex-module-decorators"
import { PageModel, PageSectionModel } from "~/utils/entities/editor/page"
import { service } from "~/utils"

@Module({
  name: 'editor',
  stateFactory: true,
  namespaced: true,
})
class EditorModule extends VuexModule {
  public page: PageModel | null = null

  get currentPage () {
    return this.page
  }

  @Mutation public GET_PAGE_DETAILS(page: PageModel) { this.page = page }
  @Mutation public ADD_PAGE_SECTION(payload) { this.page && this.page.page_section.splice(payload.index + 1, 0, payload.data) }

  @Action({ rawError: true, commit: 'GET_PAGE_DETAILS' })
  public async getPageDetails (id) {
    const res = await service.editor.getPageDetails(id)
    return res.data.data
  }

  @Action({ rawError: true })
  public async savePageDetails(page) {
    const res = await service.editor.savePageDetails(page)
    if (res.status === 200) {
      this.page = page
    }
    return res
  }

  @Action({ rawError: true })
  public async addPageSection({ index, pageId }) {
    const res = await service.editor.addPageSection({
      section_type: 'editor',
      page_id: pageId,
      nodes: []
    } as PageSectionModel)
    if (res.status === 200) {
      this.context.commit('ADD_PAGE_SECTION', { data: res.data.data, index })
    }
    return res
  }
}

export default EditorModule
