import { Module, VuexModule, Action, Mutation } from "vuex-module-decorators"
import { PageModel, PageSectionModel } from "~/utils/entities/editor/page"
import { service } from "~/utils"
import { v4 as uuidV4 } from 'uuid'
import _ from 'lodash'

@Module({
  name: 'editor',
  stateFactory: true,
  namespaced: true,
})
class EditorModule extends VuexModule {
  public page: PageModel | null = null
  public currentPageSectionId: string | null = null
  public currentNodeId: string | null = null

  get currentPage () {
    return this.page
  }

  get currentPageSection () {
    if (!this.currentPageSectionId || !this.page || !this.page.page_section) return null
    const sections = this.page.page_section.filter(section => section.id === this.currentPageSectionId)
    if (!sections || sections.length < 1) {
      return null
    }

    return sections[0]
  }

  @Mutation public CHOOSE_PAGE_SECTION(id: string) { this.currentPageSectionId = id }
  @Mutation public GET_PAGE_DETAILS(page: PageModel) { this.page = page }
  @Mutation public ADD_PAGE_SECTION(payload) { this.page && this.page.page_section.splice(payload.index + 1, 0, payload.data) }
  @Mutation public ADD_NODE(payload) {
    const section = this.page && this.page.page_section.filter(cur => cur.id === payload.sectionId)
    if (!section || section.length < 1) return

    section[0].nodes.push(payload.node)
  }
  @Mutation public DELETE_NODE(payload) {
    const section = this.page && this.page.page_section.filter(id => id === payload.sectionId)
    if (!section || section.length < 1) return

    section[0].nodes = section[0].nodes.filter(node => node.id !== payload.nodeId)
  }
  @Mutation public MODIFY_NODE(payload) {
    const section = this.page && this.page.page_section.filter(id => id === payload.sectionId)
    if (!section || section.length < 1) return

    section[0].nodes = section[0].nodes.filter(node => {
      if (node.id === payload.nodeId) {
        return payload.node
      }
      return node
    })
  }

  @Action({ rawError: true, commit: 'CHOOSE_PAGE_SECTION' })
  public async choosePageSection(id) {
    return id
  }

  @Action({ rawError: true, commit: 'GET_PAGE_DETAILS' })
  public async getPageDetails (id) {
    const res = await service.editor.getPageDetails(id)
    return res.data.data
  }

  @Action({ rawError: true })
  public async savePageDetails() {
    const page = _.cloneDeep(this.page)
    if (!page) return
    const id = page.id
    delete page.id
    delete page.key
    delete page.unique_id
    delete page.application_id

    if (!page.type) page.type = 'editor'
    return await service.editor.savePageDetails(id, page)
  }

  @Action({ rawError: true })
  public async addPageSection({ index, pageId }) {
    const res = await service.editor.addPageSection({
      section_type: 'editor',
      page_id: pageId,
      nodes: []
    })
    if (res.status === 200) {
      this.context.commit('ADD_PAGE_SECTION', { data: res.data.data, index })
    }
    return res
  }

  @Action({ rawError: true, commit: 'ADD_NODE' })
  public async addNode(node) {
    let sectionId = this.currentPageSectionId
    if (!sectionId && this.page) {
      sectionId = this.page.page_section[0].id
    }
    node.id = uuidV4() // Generate node id
    return { sectionId, node }
  }

  @Action({ rawError: true, commit: 'DELETE_NODE' })
  public async deleteNode({ sectionId, nodeId }) {
    return { sectionId, nodeId }
  }

  @Action({ rawError: true, commit: 'MODIFY_NODE' })
  public async modifyNode({ sectionId, node }) {
    return { sectionId, node }
  }
}

export default EditorModule
