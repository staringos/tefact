export default (request) => {
  return {
    getEntityConfig: (key) => request({
      url: `/page/entity/${key}`,
      method: 'get',
    }),
    deleteRowData: (id, orgId, entityId) => request({
      url: `/page/section/entity/${entityId}`,
      method: 'delete',
      data: { org_id: orgId, data_id: id },
    }),
    getEditorOptions: (entityId, orgId) => request({
      url: `/page/section/entity/${entityId}/option`,
      params: { org_id: orgId },
    }),
    getPage: (pageKey, params, orgId) => request({
      url: `/page/${pageKey}`,
      method: 'get',
      params: { ...params, org_id: orgId },
    }),

    pageModifier: (entityId, params, dataId) => request({
      url: `/page/section/entity/${entityId}`,
      method: dataId ? 'put' : 'post',
      data: {
        data: params,
        data_id: dataId,
      },
    }),

    querySectionData: (pageSectionId, page, searchCondition, sort, params, orgId) => {
      const data =  {
        page,
      } as any

      if (params) data.params = params
      if (searchCondition) data.search_condition = searchCondition
      if (sort) data.sort = sort
      if (orgId) data.org_id = orgId

      return request({
        url: `/page/section/${pageSectionId}`,
        method: 'post',
        data,
      })
    },
  }
}
