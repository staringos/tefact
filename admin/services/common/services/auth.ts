import { LoginParams, LoginEntity, PwdLoginParams } from '../'

export default (request) => {
  return {
    register: (data) => request({
      url: '/auth/register/username',
      method: 'post',
      data
    }),

    verifyCode: () => request({
      url: '/auth/verify-code',
      method: 'get',
    }),

    passwordLogin: (params) => request({
      url: '/auth/login',
      data: params,
      method: 'post',
    }),

    login: (params: LoginParams) => request({
      url: '/auth/phone/login',
      data: params,
      method: 'post',
    }),

    pwdLogin: (params: PwdLoginParams) => request({
      url: '/auth/login',
      data: params,
      method: 'post',
    }),

    verification: (params: LoginEntity) => request({
      url: '/auth/phone/code',
      data: params,
      method: 'post',
    }),

    verifyImage: () => request({
      url: '/auth/verify-code',
      method: 'get',
    }),
  }
}
