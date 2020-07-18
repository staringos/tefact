import { Module, VuexModule, Mutation, Action } from 'vuex-module-decorators'
import { User } from "~/services/common"
import { auth } from "~/utils"
// import * as authServices from "~/services/auth"
// import * as userServices from "~/services/user"
import { service } from '~/utils'
import { RegisterParams } from "~/services/common/entities/user"

interface LoginResult {
  user: User,
  access_token: string,
  refreshToken?: string
}

@Module({
  name: 'user',
  stateFactory: true,
  namespaced: true,
})
class UserModule extends VuexModule {
  public userDetailsVisible = false
  public user: User | null = null
  public access_token: string | null = null

  get currentUser() { return this.user }
  get getUserInfo() { return this.user }
  get checkLoginStatus() { return !!this.access_token }
  get userDetailsVisibleGetter() { return this.userDetailsVisible }

  @Mutation
  public LOGIN_RESULT({ user, access_token }: LoginResult) {
    this.user = user
    this.access_token = access_token
  }

  @Mutation public REFRESH_USER_DETAILS(val) { this.user = val }

  @Mutation public SET_USER_DETAILS_DIALOG(val) { this.userDetailsVisible = val }

  @Action({ rawError: true })
  public exitOrg(id) {
    return service.user.exitOrg(id)
  }

  @Action
  public readMessage(id) {
    return service.user.readMessage(id)
  }

  @Action({ commit: 'SET_USER_DETAILS_DIALOG' })
  public toggleUserDetailsDialog(val) {
    return val
  }

  @Action({ rawError: true })
  public async passwordLogin(params: any) {
    const res = await service.auth.passwordLogin(params)
    auth.setToken(res.data.data.access_token)

    if (res.status === 200)
      this.context.commit('LOGIN_RESULT', res.data.data)

    return res
  }

  @Action({ rawError: true })
  public async register(params: RegisterParams) {
    return service.auth.register(params)
  }

  @Action({ rawError: true })
  public async login(params: any) {
    const res = await service.auth.login(params)
    auth.setToken(res.data.data.access_token)

    if (res.status === 200)
      this.context.commit('LOGIN_RESULT', res.data.data)

    return res
  }

  @Action({ rawError: true })
  public async verification(params: any) {
    return service.auth.verification(params)
  }

  @Action({ rawError: true })
  public async verifyCode() {
    return service.auth.verifyCode()
  }

  @Action
  public getMessage(params) {
    return service.user.getMessage(params)
  }

  @Action
  public editUser(params) {
    return service.user.editUser(params)
  }

  @Action({ commit: 'REFRESH_USER_DETAILS' })
  public async refreshUserDetails() {
    const res = await service.user.getUserDetails()
    return res.data.data
  }
}

export default UserModule
