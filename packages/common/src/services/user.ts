import { MessageParams } from '../'
import omitBy from 'lodash/omitBy'
import isNull from 'lodash/isNull'

export default (request) => {
  return {
    getMessage: (params: MessageParams) => request({
      url: '/user/message',
      params,
    }),

    readMessage: (id) => request({
      url: `/user/message/${id}`,
      method: 'put',
    }),

    exitOrg: (orgId) => request({
      url: `/user/org/${orgId}`,
      method: 'delete',
    }),

    editUser: (data) => request({
      url: `/user/info`,
      method: 'put',
      data: omitBy(data, item => isNull(item)),
    }),

    getUserDetails: () => request({
      url: '/user/info',
    }),
  }
}
