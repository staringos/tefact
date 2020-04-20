import { BasePage } from '../base'

export interface UserParams {
  nickname: string
  signature: string
  email: string
  gender: string
  head_url: string
}

export const DefaultUserParams: UserParams = {
  nickname: '',
  signature: '',
  email: '',
  gender: '',
  head_url: ''
}

export interface UserInfo {
  email: string
  gender: number
  head_url: string
  id: string
  signature: string
}

export interface User {
  id?: string
  name?: string
  nickname?: string
  phone: number | string
  user_info?: UserInfo
}

export interface Message {
  id: string,
  content: string
}

export interface MessageParams extends BasePage {
  has_detail
  org_id?: string
}

export interface LoginEntity {
  phone?: string,
  phone_code?: string,
}

export interface LoginParams {
  phone: string
  phone_code: string
}

export interface PwdLoginParams {
  phone: string
  password: string
  verify_code: string
  uuid: string
}
