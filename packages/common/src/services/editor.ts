export default (request) => {
  return {
    getPageDetails: (id) => request({
      url: `/app/light/page/${id}`,
      method: 'get',
    }),
    savePageDetails: (page) => request({
      url: `/app/light/page/${page.id}`,
      method: 'put',
      data: page
    }),
    addPageSection: (pageSection) => request({
      url: `/app/light/page/${pageSection.page_id}/section`,
      method: 'post',
      data: pageSection
    }),
    deletePageSection: (pageId, pageSection) => request({
      url: `/app/light/page/${pageId}/section`,
      method: 'post',
      data: pageSection
    }),
  }
}
