import request from '../utils/request'

export const getAllApps = (orgId, isAll) => request({
  url: `/org/${orgId}/app?is_all=${isAll}`,
  method: 'get'
})

export const getAllOrgs = hasDetails => request({
  url: `/org/list?has_detail=${hasDetails}`,
  method: 'get'
})

export const addApp = (appId, orgId) => request({
  url: `/org/${orgId}/app/${appId}`,
  method: 'post'
})

export const removeApp = (appId, orgId) => request({
  url: `/org/${orgId}/app/${appId}`,
  method: 'delete'
})
