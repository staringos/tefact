import { GET_ALL_ORGS, SET_CURRENT_ORG } from '../constants/org'
import { service, ActionWrapper } from '../utils'
import { getAllApps } from './app'

export const currentOrgGetter = (org) =>
  ((org.orgs && org.orgs.length > 0) ? org.orgs.filter(item => item.id === org.currentOrgId)[0] : null)

export const removeStaff = ActionWrapper((_dispatch, { orgId, staffId }) =>
  service.org.removeStaff(orgId, staffId))

export const addStaff = ActionWrapper((_dispatch, staff) =>
  service.org.addStaff(staff))

export const getAllStaffs = ActionWrapper((_dispatch, { orgId, departmentId }) =>
  service.org.getStaffs(orgId, departmentId))

export const getAuth = ActionWrapper((_dispatch, orgId) =>
  service.org.getAuth(orgId))

export const saveRoleAuth = ActionWrapper((_dispatch, { roleId, orgId, auth }) =>
  service.org.saveRoleAuth(roleId, orgId, auth))

export const getRoleAuth = ActionWrapper((_dispatch, { roleId, orgId }) =>
  service.org.getRolesAuth(roleId, orgId))

export const getRoles = ActionWrapper((_dispatch, orgId) =>
  service.org.getRoles(orgId))

export const modifyRole = ActionWrapper((_dispatch, { orgId, roleName, roleId }) =>
  service.org.modifyRole(!!roleId, orgId, roleName, roleId))

export const deleteRole = ActionWrapper((_dispatch, { orgId, roleId }) =>
  service.org.deleteRole(roleId, orgId))

export const addDepartment = ActionWrapper((_dispatch, { orgId, departmentName, parentDepartmentId }) => {
  return service.org.addDepartment(orgId, departmentName, parentDepartmentId)
})

export const modifyDepartment = ActionWrapper((_dispatch, { orgId, departmentName, id }) => {
  return service.org.modifyDepartment(orgId, departmentName, id)
})

export const deleteDepartment = ActionWrapper((_dispatch, { orgId, departmentId }) => {
  return service.org.deleteDepartment(orgId, departmentId)
})

export const getAllDepartment = ActionWrapper((_dispatch, params) => {
  return service.org.getAllDepartment(params)
})

export const getAllOrgs = ActionWrapper(async (dispatch) => {
  const res = await service.app.getAllOrgs(1)
  const data = res.data.data

  dispatch({ type: GET_ALL_ORGS, data })

  return data
})

export const setCurrentOrg = ActionWrapper(async (dispatch, id) => {
  dispatch({ type: SET_CURRENT_ORG, data: id })
  await getAllApps(dispatch)({ id, isAll: 0 })
})

export const modifyOrg = ActionWrapper(async (dispatch, data) => {
  let res: any = null
  if (data.id) res = await service.org.modifyOrg(data)
  else res = await service.org.createOrg(data)

  if (res && res.statusCode === 200) getAllOrgs(dispatch)()

  return res
})
