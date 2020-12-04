import axios from 'axios'
import Tools, { auth } from '~/utils'

export const uploadImageUrl = `${process.env.ARRPLAT_BASE_URL}/core/upload-files/${process.env.BUCKET_NAME}`

// create an axios instance
const service = axios.create({
  baseURL: process.env.ARRPLAT_BASE_URL, // url = base url + request url
  withCredentials: true, // send cookies when cross-domain requests
  timeout: 100000 // request timeout
})

export const codeMessage = {
  400: '请求错误',
  401: '未授权，请登录',
  422: '未授权，请登录',
  403: '拒绝访问',
  404: `请求地址出错`,
  408: '请求超时',
  500: '服务器内部错误',
  501: '服务未实现',
  502: '网关错误',
  503: '服务不可用',
  504: '网关超时',
  505: 'HTTP版本不受支持'
} as object

// request interceptor
service.interceptors.request.use(
  config => {
    const token = auth.getToken()

    if (token)
      config.headers['Authorization'] = `Bearer ${auth.getToken()}`


    return config
  },
  error => {
    // do something with request error
    return Promise.reject(error)
  }
)

// response interceptor
service.interceptors.response.use(
  response => {
    return response
  },
  error => {
    console.log('hererrr', error)
    if (error.response.status === 401) {
      auth.setToken('')
      if (global) return {}
      if (window) window.location.href = '/auth'
    }
    return Promise.reject(error.response)
  }
)

export default (params: any) => {
  if (params.ctx && params.ctx.req && params.ctx.req.headers) {
    const token = Tools.getCookie(params.ctx.req.headers.cookie, auth.TokenKey)
    if (token && token.length > 1)
      params.headers = {
        ...params.headers,
        Authorization: `Bearer ${token}`
      }

  }

  return service(params)
}
