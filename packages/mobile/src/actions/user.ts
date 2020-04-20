import { ActionWrapper, service } from '../utils'
import { GET_USER_DETAILS, GET_ALL_MESSAGE } from '../constants/user'

export const getUserInfo = ActionWrapper(async (dispatch) => {
  const res = await service.user.getUserDetails()

  if (res.statusCode !== 200) {
    throw res.data
  }

  dispatch({
    type: GET_USER_DETAILS,
    data: res.data.data,
  })

  return res.data
})

export const editUser = ActionWrapper(async (dispatch, userParams) => {
  const res = await service.user.editUser(userParams)

  if (res.statusCode === 200)
    getUserInfo(dispatch)()

  return res
})

export const getAllMessages = ActionWrapper(async () => {
  const res = await service.user.getMessage({ has_detail: 1 })

  return {
    type: GET_ALL_MESSAGE,
    data: res.data.data,
  }
})

export const setMessageAsRead  = ActionWrapper(async (dispatch, id) => {
  const res = await service.user.readMessage(id)

  if (res.statusCode === 200) {
    getAllMessages(dispatch)()
  }
  return res
})
