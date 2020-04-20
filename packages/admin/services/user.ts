import request from "~/utils/request"
import { MessageParams } from '@arrplat/common'
import _ from 'lodash'

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
  data: _.omitBy(data, item => _.isNull(item))
})

export const getUserDetails = () => request({
  url: '/user/info'
})
