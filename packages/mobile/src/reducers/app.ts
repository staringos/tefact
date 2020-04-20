import { GET_ALL_APPS, GET_ORG_APPS, SET_CURRENT_APP } from '../constants/app';

const  INITIAL_STATE = {
  currentAppId: null,
  apps: [],
  allApps: [],
}

export default function app(state = INITIAL_STATE, action) {
  switch (action.type) {
    case GET_ALL_APPS:
      return { ...state, allApps: action.data }
    case GET_ORG_APPS:
      const id = action.data && action.data.length > 0 ? action.data[0].id : null
      const currentAppId = (state.currentAppId ? state.currentAppId : id)
      return { ...state, apps: action.data, currentAppId }
    case SET_CURRENT_APP:
      return { ...state, currentAppId: action.data }
    default:
      return state
  }
}
