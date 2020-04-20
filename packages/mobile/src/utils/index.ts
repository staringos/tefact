import Taro from '@tarojs/taro'
import { ServiceGenerator } from '@arrplat/common'

const tokenKey = 't'

export const loop = (data) => data ? data.map(item => {
  const isLeaf = item.child_org_departments.length < 1

  return ({
    label: item.name,
    value: item.id,
    isLeaf,
    disabled: false,   // 是否禁用
    children: isLeaf ? [] : loop(item.child_org_departments),
  })
}) : []

export function getSubtract(unionArr, subsetArr, key = 'id') {
  const newTmp = [] as any[]
  unionArr.map(item => {
    let exists = false
    subsetArr.forEach(subItem => {
      if (item[key] === subItem[key]) exists = true
    })
    if (!exists) newTmp.push(item)
  })
  return newTmp
}

export const AuthStorage = {
  setToken(data) {
    Taro.setStorageSync(tokenKey, data)
  },
  getToken() {
    return Taro.getStorageSync(tokenKey)
  },
  clearToken() {
    Taro.clearStorageSync()
  },
}

export const UI = {
  bind(that, key) {
    const keys = key.split('.')

    if (keys.length === 1) {
      return (event) => { that.setState({ [key]: (event.target as any).value }) }
    }

    return (event) => {
      that.setState({ [keys[0]]: { ...that.state[keys[0]], [keys[1]]: (event.target as any).value } })
    }
  },
  bindTaroUI(that, key) {
    const keys = key.split('.')

    if (keys.length === 1) {
      return (event) => { that.setState({ [key]: event }) }
    }

    return (event) => {
      that.setState({ [keys[0]]: { ...that.state[keys[0]], [keys[1]]: event } })
    }
  },
}

// export const baseUrl = 'https://arrplatapi.arrway.cn/api'
export const baseUrl = '127.0.0.1:5500/api'
export const imageUploadUrl = `${baseUrl}/core/upload-files/arrplat`
// const baseUrl = 'http://localhost:5500'

const request = (options) => {
  if (options.url && options.url.indexOf('http') === -1) {
    options.url = `${baseUrl}${options.url}`
  }

  const token = AuthStorage.getToken()

  if (options.params) {
    options.data = { ...options.data, ...options.params }
  }

  if (token) {
    const additional = { Authorization: `Bearer ${token}` }
    if (options.header) {
      options.header = { ...options.header, ...additional }
    } else {
      options.header = additional
    }
  }

  if (!options.fail) {
    options.fail = (e) => {
      console.log('on fail e:', e)
    }
  }

  return Taro.request(options).catch(e => {
    console.log('on catchhhhhh e:', e)
  })
}

export const service = ServiceGenerator(request)

export const ActionWrapper: Function = (action) => (dispatch) => async (params) => {
  const res = await action(dispatch, params)
  if (res && res.type) {
    dispatch(res)
  }

  return res
}
