import ServiceGenerator from '../services/common/services'
import request from './request'
import Tools from "./tools"
import responseLib from "./BaseResponse"
import * as authLib from "./auth"

export default Tools

export const response = responseLib
export const auth = authLib
export const service = ServiceGenerator(request)

export const generateMysqlConnectUrl = ({ address, port, dbName, username, password }: any) => {
  return `jdbc:mysql://${address}:${port}/${dbName}?user=${username}&password=${password}'`
}

export const hasMetaKeyPass = () => {
  return window && window.event && (window.event['ctrlKey'] || window.event['metaKey'])
}

// export const gotoAppIndex = (app, router) => {
//   if (app.type === 'light')
//     return router.push(`/light/${app.admin_route}`)
//
//   router.push(`/plugins/${app.admin_route}`)
// }

export const findPrimaryKey = (fields) => {
  const primary = fields.filter(res => res.is_primary)
  if (primary.length > 0)
    return primary[0].key

  return null
}

export function deepCopy(obj) {
  return JSON.parse(JSON.stringify(obj))
}

export function transformTime(timestamp = +new Date(), type = 'datetime') {
  if (!timestamp) return

  const time = new Date(timestamp)

  const y = time.getFullYear()
  const M = time.getMonth() + 1
  const d = time.getDate()
  const h = time.getHours()
  const m = time.getMinutes()
  const s = time.getSeconds()

  if (type === 'datetime')
    return y + '-' + M + '-' + d + ' ' + h + ':' + m + ':' + s
  if (type === 'date')
    return y + '-' + M + '-' + d
  if (type === 'time')
    return ' ' + h + ':' + m + ':' + s
}

export function checkPhone(phone) {
  const myReg =/^1([38][0-9]|4[579]|5[0-3,5-9]|6[6]|7[0135678]|9[89])\d{8}$/
  if (!myReg.test(phone)) return false
  return  true
}

const FindParamsReg = new RegExp('[$]{([^}#]+)}')

export function wrapParamsObject(str, obj) {
  let query = str.match(FindParamsReg)
  let tmp = str
  const res = {}

  while (query) {
    const arr = tmp.split(' ')
    const key = arr[0].split('=')[0]
    tmp = tmp.replace(`${key}=${query[0]}`, '')
    res[key] = obj[query[1]]
    query = tmp.match(FindParamsReg)
  }

  return res
}

export function extractParams(str, obj) {
  let query = str.match(FindParamsReg)
  let tmp = str
  const res = {}

  while (query) {
    tmp = tmp.replace(query[0], ' ')
    res[query[1]] = obj[query[1]]
    query = tmp.match(FindParamsReg)
  }

  return res
}

export function wrapParams(str, obj) {
  if (!str) return ''

  let query = str.match(FindParamsReg)
  let tmp = str

  while (query) {
    tmp = tmp.replace(query[0], obj[query[1]])
    query = tmp.match(FindParamsReg)
  }

  return tmp
}
