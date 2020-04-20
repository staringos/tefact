import { User } from './user'

export interface Org {
  orgName?: string,
  orgId?: string,
  orgDescribe?: string
}

export interface OrgParams {
  name: string
  unique_id: string
  description: string
  group_type?: string
  address?: string
}

export const DefaultOrgParams:OrgParams =  {
  name: '',
  unique_id: '',
  description: '',
}

export interface Department {
  label: string
  id: string
  children: Department[]
}

export interface Staff {
  id: string
  is_able: boolean
  job_title: string
  org_department_staff: Department[]
  parent_superior: string
  user: User
}

export interface StaffParams {
  id?: string
  is_able: boolean
  job_title: string
  department_id_list: string[]
  superior_id: string
  role_id_list: string[]
}


export const DefaultUser = {
  phone: ''
} as User

export const DefaultStaff = {
  id: '',
  is_able: true,
  job_title: '',
  org_department_staff: [],
  parent_superior: '',
  user: {
    ...DefaultUser
  }
}

export interface OrgConfig {
  id?: string
}

export interface Role {
  name: string
  id: string
}

export const DefaultRole:Role = {
  name: '',
  id: ''
}

export interface Auth {
  name: string
  id: string
  icon: string
  function: string
  type: string
  children: Auth[]
}
