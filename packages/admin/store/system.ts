import { Module, VuexModule, Mutation, Action } from 'vuex-module-decorators'
import { auth } from '@arrplat/utils'
import { uploadImageUrl } from '~/utils/request'

export const DIALOG_NAME: any = {
  USER_MODIFY_DIALOG: 'USER_MODIFY_DIALOG',
  CREATE_ORG: 'CREATE_ORG',
  NO_ORG_DIALOG: 'NO_ORG_DIALOG',
  LIGHT_APP_MODIFY_DIALOG: 'LIGHT_APP_MODIFY_DIALOG',
}

const initVisible = {}

for (const key in DIALOG_NAME)
  initVisible[DIALOG_NAME[key]] = false

@Module({
  name: 'system',
  stateFactory: true,
  namespaced: true,
})
export default class SystemModule extends VuexModule {
  public dialogsVisible: any = { ...initVisible }
  public showPluginMenu = true
  public uploadImageUrl: string = uploadImageUrl

  get dialogsVisibleGetter() { return this.dialogsVisible }
  get showPluginMenuGetter() { return this.showPluginMenu }
  get uploadUrl() { return this.uploadImageUrl }

  @Mutation public SET_DIALOG_VISIBLE({ key, visible }) {
    this.dialogsVisible = { ...this.dialogsVisible, [key]: visible }
  }
  @Mutation public TOGGLE_PLUGIN_MENU() { this.showPluginMenu = !this.showPluginMenu }

  @Action({ commit: 'TOGGLE_PLUGIN_MENU' })
  public togglePluginMenu() {
    return
  }

  @Action({ commit: 'SET_DIALOG_VISIBLE' })
  public setDialogVisible({ key, visible }) {
    return { key, visible }
  }

  @Action({ commit: 'SET_DIALOG_VISIBLE' })
  public exit() {
    auth.removeToken()
    localStorage.clear()
    sessionStorage.clear()
    location.href = '/login'
  }
}
