import { auth } from '@arrplat/utils'
import createPersistedState from 'vuex-persistedstate'
import { Plugin } from '@nuxt/types'

interface MyWindow extends Window {
  onNuxtReady(obj: object): void
}
declare var window: MyWindow

const PersistedState: Plugin = ({ store, isHMR }) => {
  if (isHMR) return

  const key = 'ns'
  const storage = localStorage
  const context = storage.getItem(key)

  const token = auth.getToken()

  // If cookie expired, clear storage
  if ((!token || token.length < 1) && context && context.indexOf('accessToken') > -1) {
    try {
      const state = JSON.parse(context)
      if (state.user.accessToken && state.user.accessToken.length > 0) {
        state.user = state.user.state()
        console.log('state.user:', state.user)
        localStorage.removeItem(key)
      }
    } catch (e) {
      console.log('state with nothing:', e)
    }
  }

  window.onNuxtReady(() => {
    createPersistedState({
      key,
      paths: ['user'],
      storage
    })(store)
  })
}

export default PersistedState
