import * as Cookies from 'js-cookie'

export const TokenKey = 't'
const expires = new Date(new Date().getTime() + (3 * 24 * 60 * 60 * 1000))

export function getToken() {
  return Cookies.get(TokenKey)
}

export function setToken(token: string) {
  return Cookies.set(TokenKey, token, {
    expires
  })
}

export function removeToken() {
  return Cookies.remove(TokenKey)
}
