export default (request) => {
  return {
    getDataSource: (appId) => request({
      url: `/app/light/${appId}/data-source`,
      method: 'get',
    }),
    deletePage: id => request({
      url: `/app/light/page/${id}`,
      method: 'delete'
    }),
    addPage: (data) => request({
      url: `/app/light/page`,
      method: 'post',
      data,
    }),
    sharePage: (pageId, type) => request({
      url: `/s/p/${pageId}`,
      method: 'post',
      data: {
        type
      },
    }),

    getSharePageInfo: key => request({
      url: `/s/p/${key}`,
      method: 'get'
    }),

    getSharePageDetails: (key, pwd?) => request({
      url: `/s/p/${key}/d`,
      method: 'post',
      data: {
        pwd
      }
    }),

    addMenu: (data) => request({
      url: `/app/light/menu`,
      method: 'post',
      data,
    }),
    deleteMenu: (id) => request({
      url: `/app/light/menu/${id}`,
      method: 'delete'
    }),
    modifyMenu: (id, data) => request({
      url: `/app/light/menu/${id}`,
      method: 'put',
      data
    }),
    getAppDetails: (appId) => request({
      url: `/app/light/${appId}`,
      method: 'get',
    }),
    removeLightApp: (appId) => request({
      url: `/app/light/${appId}`,
      method: 'delete',
    }),
    lightAppAdd: (data) => request({
      url: `/app/light`,
      method: 'post',
      data,
    }),
    getAppById: (orgId, appId) => request({
      url: `/org/${orgId}/app/${appId}`,
      method: 'get',
    }),
    getAllApps: (orgId, isAll, platform = 'pc') => request({
      url: `/org/${orgId}/app?is_all=${isAll}&platform=${platform}`,
      method: 'get',
    }),
    getAllOrgs: (hasDetails) => request({
      url: `/org/list?has_detail=${hasDetails}`,
      method: 'get',
    }),
    addApp: (appId, orgId) => request({
      url: `/org/${orgId}/app/${appId}`,
      method: 'post',
    }),
    modifyApp: (appId, app) => request({
      url: `/app/light/${appId}`,
      method: 'put',
      data: app
    }),
    removeApp: (appId, orgId) => request({
      url: `/org/${orgId}/app/${appId}`,
      method: 'delete',
    }),
  }
}
