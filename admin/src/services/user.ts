import request from "~/utils/request"
import { MessageParams } from '~/services/common/entities/user'
import omitBy from 'lodash/omitBy'
import isNull from 'lodash/isNull'

export const getMessage = (params: MessageParams) => request({
  url: '/user/message',
  params: params
})

export const readMessage = (id) => request({
  url: `/user/message/${id}`,
  method: 'put'
})

export const exitOrg = (orgId) => request({
  url: `/user/org/${orgId}`,
  method: 'delete'
})

export const editUser = (data) => request({
  url: `/user/info`,
  method: 'put',
  data: omitBy(data, item => isNull(item))
})

export const getUserDetails = () => request({
  url: '/user/info'
})
