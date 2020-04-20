import { combineReducers } from 'redux'
import counter from './counter'
import user from './user'
import app from './app'
import org from './org'
import system from './system'

export default combineReducers({
  counter,
  user,
  app,
  system,
  org,
})
