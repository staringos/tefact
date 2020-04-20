import { Store } from 'vuex'
import { getModule } from 'vuex-module-decorators'
import app from '../store/app'
import user from '../store/user'
import org from '../store/org'
import system from '../store/system'
import entities from '../store/entities'
import platform from '../store/platform'
import education from '../store/education'

let systemStore: any = null
let appStore: any = null

function initialiseStores(store: Store<any>): void {
  appStore = getModule(app, store)
  getModule(user, store)
  getModule(org, store)
  getModule(entities, store)
  getModule(platform, store)
  getModule(education, store)
  systemStore = getModule(system, store)
}

export {
  initialiseStores,
  systemStore,
  appStore,
}
