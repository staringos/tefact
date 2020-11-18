import entities from './entities'
import { OrgParams, Role } from "~/services/common/entities/org"
import { User, UserParams } from "~/services/common/entities/user"

export default {
  entities,
}

export const DefaultOrgParams: OrgParams =  {
  name: '',
  unique_id: '',
  description: '',
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

export const DefaultRole: Role = {
  name: '',
  id: ''
}

export const DefaultUserParams: UserParams = {
  nickname: '',
  signature: '',
  email: '',
  gender: '',
  head_url: ''
}
