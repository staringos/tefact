import { OrgParams } from '~/services/common/entities/org'
import omitBy from 'lodash/omitBy'
import isNull from 'lodash/isNull'

export default (request) => {
  return {
    createOrg: (org: OrgParams) => request({
      url: '/org',
      method: 'post',
      data: org
    }),
    modifyOrg: (org) => request({
      url: `/org/${org.id}`,
      method: 'put',
      data: omitBy(org, item => isNull(item)),
    }),
    getRoles: (orgId) => request({
      url: `/org/${orgId}/role`,
      method: 'get',
    }),
    deleteDepartment: (orgId, departmentId) => request({
      url: `/org/${orgId}/department/${departmentId}`,
      method: 'delete',
    }),
    modifyDepartment: (orgId, dependenceName, id) => {
      const data = {
        name: dependenceName,
      }

      return request({
        url: `/org/${orgId}/department/${id}`,
        method: 'put',
        data,
      })
    },
    addDepartment: (orgId, dependenceName, parentDepartmentId) => {
      const data = {
        name: dependenceName,
        parent_department_id: parentDepartmentId,
      }

      if (parentDepartmentId === '-1') delete data.parent_department_id

      return request({
        url: `/org/${orgId}/department`,
        method: 'post',
        data,
      })
    },
    getStaffs: (orgId, departmentId) => request({
      url: `/org/${orgId}/department/${departmentId}/staff`,
      method: 'get',
    }),
    modifyStaff: (staff) => request({
      url: `/org/${staff.orgId}/staff/${staff.id}`,
      method: 'put',
      data: staff.data,
    }),
    addStaff: (staff) => request({
      url: `/org/${staff.orgId}/staff`,
      method: 'post',
      data: staff.data,
    }),
    removeStaff: (orgId, staffId) => request({
      url: `/org/${orgId}/staff/${staffId}`,
      method: 'delete',
    }),
    getAllDepartment: (orgId) => request({
      url: `/org/${orgId}/department/list`,
      method: 'get',
    }),
    modifyRole: (isEdit, orgId, roleName, roleId) => {
      const data = {
        name: roleName,
      } as any

      return request({
        url: `/org/${orgId}/role${isEdit ? '/' + roleId : ''}`,
        method: isEdit ? 'put' : 'post',
        data,
      })
    },
    deleteRole: (roleId, orgId) => request({
      url: `/org/${orgId}/role/${roleId}`,
      method: 'delete',
    }),
    deleteRoleStaff: (roleId, orgId, staffId) => request({
      url: `/org/${orgId}/role/${roleId}/staff`,
      method: 'delete',
      data: {
        staff_id: staffId,
      },
    }),
    getRolesStaff: (roleId, orgId) => request({
      url: `/org/${orgId}/role/${roleId}/staff`,
    }),
    getRolesAuth: (roleId, orgId) => request({
      url: `/org/${orgId}/role/${roleId}/auth`,
    }),
    getAuth: (orgId) => request({
      url: `/org/${orgId}/auth`,
    }),
    saveRoleAuth: (roleId, orgId, auth) => request({
      url: `/org/${orgId}/role/${roleId}/auth`,
      method: 'put',
      data: {
        config_id_list: auth,
      },
    }),
    saveRoleStaff: (roleId, orgId, staffIds) => request({
      url: `/org/${orgId}/role/${roleId}/staff`,
      method: 'put',
      data: {
        staff_id_list: staffIds,
      },
    }),
  }
}
