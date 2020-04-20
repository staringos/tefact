import { LOGIN_SUCCESS } from "../constants/user";
import { service, ActionWrapper, AuthStorage } from '../utils'
import { init } from './system'

export const bindAccount = ActionWrapper(async (dispatch, params) => {
  const res = await service.auth.pwdLogin(params)

  if (res.statusCode !== 200) {
    throw res.data
  }
  const data = res.data.data
  AuthStorage.setToken(data.access_token)

  dispatch({ type: LOGIN_SUCCESS, data })
  await init(dispatch)()
})
