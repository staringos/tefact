import { CLOSE_DIALOG, OPEN_DIALOG } from '../constants/system'
import { LOGIN_SUCCESS, LOGOUT } from '../constants/user'
import { ActionWrapper, AuthStorage } from '../utils'

import * as userActions from './user'
import * as orgActions from './org'

export const init = ActionWrapper(async (dispatch) => {
  const token = AuthStorage.getToken()
  if (!token) { return }

  dispatch({ type: LOGIN_SUCCESS, data: token })

  userActions.getUserInfo(dispatch)()
  userActions.getAllMessages(dispatch)()

  const res = await orgActions.getAllOrgs(dispatch)()
  if (res.length > 0) {
    await orgActions.setCurrentOrg(dispatch)(res[0].id)
  }
})

export const logout = ActionWrapper(() => {
  AuthStorage.clearToken()
  return { type: LOGOUT }
})

export const openDialog = ActionWrapper(({ key, value }) => ({ type: OPEN_DIALOG, data: { key, value } }))
export const closeDialog = ActionWrapper((key) => ({ type: CLOSE_DIALOG, key }))
