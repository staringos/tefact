import { User, Message } from '@arrplat/common'
import { LOGIN_SUCCESS, GET_USER_DETAILS, LOGOUT, GET_ALL_MESSAGE } from '../constants/user'

const  INITIAL_STATE = {
  accessToken: null,
  user: {} as User,
  messages: [] as Message[],
  messageUnread: 0 as number,
}

export default function user(state = INITIAL_STATE, action) {
  switch (action.type) {
    case GET_ALL_MESSAGE:
      return { ...state, messages: action.data.message_list, messageUnread: action.data.unread_count }
    case LOGOUT:
      return INITIAL_STATE
    case LOGIN_SUCCESS:
      return { ...state, accessToken: action.data }
    case GET_USER_DETAILS:
      return { ...state, user: action.data }
    default:
      return state
  }
}
