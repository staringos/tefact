import { GET_ORG_APPS, SET_CURRENT_APP, GET_ALL_APPS } from '../constants/app'
import { service, ActionWrapper } from '../utils'

export const currentAppGetter = app =>
  app.apps && app.apps.length > 0 ? app.apps.filter(current => current.id === app.currentAppId)[0] : null

export const getAppById = ActionWrapper((_dispatch, { orgId, appId }) =>
  service.app.getAppById(orgId, appId))

export const getAllApps = ActionWrapper(async (_dispatch, { id, isAll }) => {
  const res = await service.app.getAllApps(id, isAll, 'mobile')
  const data = res.data.data

  if (isAll === 0) return { type: GET_ORG_APPS, data }
  return { type: GET_ALL_APPS, data }
})

export const addApp = ActionWrapper(async (_dispatch, { appId, orgId }) => {
  const res = await service.app.addApp(appId, orgId)
  if (res.statusCode === 200) await getAllApps(_dispatch)({ id: orgId, isAll: 0 })
  return res
})

export const removeApp = ActionWrapper(async (_dispatch, { appId, orgId }) => {
  const res = await service.app.removeApp(appId, orgId)
  if (res.statusCode === 200) await getAllApps(_dispatch)({ id: orgId, isAll: 0 })
  return res
})

export const setCurrentApp = ActionWrapper(async (_dispatch, id) => {
  return {
    type: SET_CURRENT_APP,
    data: id,
  }
})
