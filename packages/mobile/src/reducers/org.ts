import { GET_ALL_ORGS, SET_CURRENT_ORG } from '../constants/org'

const  INITIAL_STATE = {
  orgs: [],
  currentOrgId: null,
}

export default function org(state = INITIAL_STATE, action) {
  switch (action.type) {
    case GET_ALL_ORGS:
      console.log('GET_ALL_ORGS action:', action)
      return { ...state, orgs: action.data }
    case SET_CURRENT_ORG:
      return { ...state, currentOrgId: action.data }
    default:
      return state
  }
}
