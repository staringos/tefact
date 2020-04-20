import request from '~/utils/request'
import { OrgParams } from '@arrplat/common'
import _ from 'lodash'

export const createOrg = (org: OrgParams) => request({
  url: '/org',
  method: 'post',
  data: org
})

export const modifyOrg = (org) => request({
  url: `/org/${org.id}`,
  method: 'put',
  data: _.omitBy(org, item => _.isNull(item))
})

export const getRoles = (orgId) => request({
  url: `/org/${orgId}/role`,
  method: 'get'
})

export const deleteDepartment = (orgId, departmentId) => request({
  url: `/org/${orgId}/department/${departmentId}`,
  method: 'delete',
})

export const addDepartment = (orgId, dependenceName, parentDepartmentId) => {
  const data = {
    name: dependenceName,
    parent_department_id: parentDepartmentId
  }

  if (parentDepartmentId === '-1') delete data.parent_department_id

  return request({
    url: `/org/${orgId}/department`,
    method: 'post',
    data
  })
}

export const getStaffs = (orgId, departmentId) => request({
  url: `/org/${orgId}/department/${departmentId}/staff`,
  method: 'get'
})

export const addStaff = (staff) => request({
  url: `/org/${staff.orgId}/staff`,
  method: 'post',
  data: staff.data
})

export const removeStaff = (orgId, staffId) => request({
  url: `/org/${orgId}/staff/${staffId}`,
  method: 'delete'
})

export const getAllDepartment = (orgId) => request({
  url: `/org/${orgId}/department/list`,
  method: 'get'
})

export const modifyRole = (isEdit, orgId, roleName, roleId) => {
  const data = {
    name: roleName
  } as any

  return request({
    url: `/org/${orgId}/role${isEdit ? '/' + roleId : ''}`,
    method: isEdit ? 'put' : 'post',
    data
  })
}

export const deleteRole = (roleId, orgId) => request({
  url: `/org/${orgId}/role/${roleId}`,
  method: 'delete',
})

export const deleteRoleStaff = (roleId, orgId, staffId) => request({
  url: `/org/${orgId}/role/${roleId}/staff`,
  method: 'delete',
  data: {
    staff_id: staffId,
  }
})

export const getRolesStaff = (roleId, orgId) => request({
  url: `/org/${orgId}/role/${roleId}/staff`
})

export const getRolesAuth = (roleId, orgId) => request({
  url: `/org/${orgId}/role/${roleId}/auth`
})

export const getAuth = (orgId) => request({
  url: `/org/${orgId}/auth`
})

export const saveRoleAuth = (roleId, orgId, auth) => request({
  url: `/org/${orgId}/role/${roleId}/auth`,
  method: 'put',
  data: {
    config_id_list: auth
  }
})

export const saveRoleStaff = (roleId, orgId, staffIds) => request({
  url: `/org/${orgId}/role/${roleId}/staff`,
  method: 'put',
  data: {
    staff_id_list: staffIds
  }
})
