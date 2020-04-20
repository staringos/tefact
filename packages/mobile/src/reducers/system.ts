import { OPEN_DIALOG, CLOSE_DIALOG, DIALOGS } from '../constants/system'

const dialogsVisible = {}

Object.values(DIALOGS).map(key => (dialogsVisible[key] = false))

const INITIAL_STATE = {
  dialogsVisible: {},
}

export default function system(state = INITIAL_STATE, action) {
  switch (action.type) {
    case OPEN_DIALOG:
      return { ...state, dialogsVisible: { ...state, [action.data.key]: action.data.value ? action.data.value : true }}
    case CLOSE_DIALOG:
      return { ...state, dialogsVisible: { ...state, [action.key]: false } }
    default:
      return state
  }
}
