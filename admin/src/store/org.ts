import { Module, VuexModule, Mutation, Action } from 'vuex-module-decorators'
import { Department, Staff, Role, Auth, OrgParams } from '~/services/common/entities/org'
import { service } from '~/utils'

function loop(department): Department[] {
  return department.map(dep => {
    const children = dep.child_org_departments && dep.child_org_departments.length > 0 ?
      loop(dep.child_org_departments) : []
    return {
      id: dep.id,
      label: dep.name,
      children,
    }
  })
}

@Module({
  name: 'org',
  stateFactory: true,
  namespaced: true,
})
export default class OrgModule extends VuexModule {
  public department: Department[] = []
  public staffs: Staff[] = []
  public roles: Role[] = []
  public auth: Auth[] = []
  public createOrgVisible = false

  get allDepartment() { return this.department }
  get allStaffs() { return this.staffs }
  get allRoles() { return this.roles }
  get allAuth() { return this.auth }
  get createOrgVisibleGetter() { return this.createOrgVisible }

  @Mutation public GET_DEPARTMENT(val) { this.department = loop(val) }
  @Mutation public GET_STAFFS(val) { this.staffs = val }
  @Mutation public GET_ROLES(val) { this.roles = val }
  @Mutation public SET_ALL_AUTH(val) { this.auth = val }
  @Mutation public SET_CREATE_ORG_DIALOG(val) { this.createOrgVisible = val }

  @Action({ commit: 'SET_CREATE_ORG_DIALOG', rawError: true })
  public toggleCreateOrgDialog(val) {
    return val
  }

  @Action({ commit: 'GET_DEPARTMENT' })
  public async getCurrentDepartment(orgId) {
    const res = await service.org.getAllDepartment(orgId)
    return res.data.data
  }

  @Action({ commit: 'GET_STAFFS' })
  public async getStaffs({ orgId, departmentId }) {
    const res = await service.org.getStaffs(orgId, departmentId)
    return res.data.data
  }

  @Action
  public async departmentModifier({ orgId, departmentName, parentDepartmentId, id }) {
    if (id)
      return service.org.modifyDepartment(orgId, departmentName, id)

    return service.org.addDepartment(orgId, departmentName, parentDepartmentId)
  }

  @Action
  public async deleteDepartment({ orgId, departmentId }) {
    return service.org.deleteDepartment(orgId, departmentId)
  }

  @Action
  public modifyStaff(staff) {
    return service.org.modifyStaff(staff)
  }

  @Action({ rawError: true })
  public addStaff(staff) {
    return service.org.addStaff(staff)
  }

  @Action
  public removeStaff({ orgId, staffId }) {
    return service.org.removeStaff(orgId, staffId)
  }

  @Action({ commit: 'GET_ROLES' })
  public async getRoles(orgId) {
    const res = await service.org.getRoles(orgId)
    return res.data.data
  }

  @Action
  public modifyRole({ isEdit, orgId, roleName, roleId }) {
    return service.org.modifyRole(isEdit, orgId, roleName, roleId)
  }

  @Action
  public getRolesStaff({ roleId, orgId }) {
    return service.org.getRolesStaff(roleId, orgId)
  }

  @Action
  public getRolesAuth({ roleId, orgId }) {
    return service.org.getRolesAuth(roleId, orgId)
  }

  @Action({ commit: 'SET_ALL_AUTH' })
  public async getAuth(orgId) {
    const res = await service.org.getAuth(orgId)
    const data = res.data.data
    return [ ...data.system_menu, ...data.application_menu ]
  }

  @Action
  public deleteRole({ roleId, orgId }) {
    return service.org.deleteRole(roleId, orgId)
  }

  @Action
  public deleteRoleStaff({ roleId, staffId, orgId }) {
    return service.org.deleteRoleStaff(roleId, orgId, staffId)
  }

  @Action
  public saveRoleAuth({ roleId, orgId, auth }) {
    return service.org.saveRoleAuth(roleId, orgId, auth)
  }

  @Action
  public saveRoleStaff({ roleId, orgId, staffIds }) {
    return service.org.saveRoleStaff(roleId, orgId, staffIds)
  }

  @Action
  public modifyOrg(org) {
    return service.org.modifyOrg(org)
  }

  @Action({ rawError: true })
  public createOrg(org: OrgParams) {
    return service.org.createOrg(org)
  }
}
