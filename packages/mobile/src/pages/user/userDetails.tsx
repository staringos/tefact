import { ComponentClass } from 'react'
import Taro from '@tarojs/taro'
import { connect } from '@tarojs/redux'
import { View } from '@tarojs/components'
import { User, UserParams, DefaultUserParams } from '@arrplat/common'
import { AtForm, AtInput, AtButton, AtAvatar } from 'taro-ui'

import AppPageLayout from '../../layout/AppPageLayout'
import { getUserInfo, editUser } from '../../actions/user'
import { UI } from '../../utils'
import '../../assets/styles/pages/user-details.scss'

type PageStateProps = {
  user: User,
}
type PageDispatchProps = {
  toGetUserInfo: () => Promise<any>,
  toEditUser: (userParams: UserParams) => Promise<any>,
}
type PageOwnProps = {}
type PageState = {
  userInfo: User,
}
type IProps = PageStateProps & PageDispatchProps & PageOwnProps

interface UserDetails {
  props: IProps
  state: PageState
}

@connect(({ user }) => ({
    user: user.user,
  }),
  (dispatch) => ({
    toGetUserInfo: getUserInfo(dispatch),
    toEditUser: editUser(dispatch),
  }),
)
class UserDetails extends Taro.PureComponent {
  public state = {
    userInfo: {
      ...DefaultUserParams,
    },
  } as PageState

  public async componentDidMount() {
    await this.refreshData()
  }

  public refreshData = async () => {
    const {toGetUserInfo} = this.props
    const res = await toGetUserInfo()
    const data = res.data
    const userInfo = {
      ...data,
      signature: data.user_info.signature,
      email: data.user_info.email,
      gender: data.user_info.gender,
    }

    this.setState({
      userInfo,
    })
  }

  public handleSubmit = async () => {
    const { toEditUser } = this.props
    const { userInfo } = this.state
    const res = await toEditUser(userInfo)

    if (res.statusCode === 200) {
      Taro.showToast({ title: `操作成功` })
      return Taro.navigateBack()
    }

    return Taro.showToast({ title: res.data.message ? res.data.message : `操作失败` })
  }

  public render() {
    const { userInfo } = this.state

    return (<AppPageLayout hasBack title="个人资料">
      <View className="avatar-area">
        <AtAvatar image={userInfo.head_url} size="large" circle />
      </View>
      <AtForm
        onSubmit={this.handleSubmit}
      >
        <AtInput
          name="phone"
          title="手机号"
          type="text"
          placeholder="请输入手机号"
          value={userInfo.phone}
          onChange={UI.bindTaroUI(this, 'userInfo.phone')}
        />
        <AtInput
          name="value"
          title="昵称"
          type="text"
          placeholder="请输入昵称"
          value={userInfo.nickname}
          onChange={UI.bindTaroUI(this, 'userInfo.nickname')}
        />
        <AtInput
          name="value"
          title="简介"
          type="text"
          placeholder="请输入简介"
          value={userInfo.signature}
          onChange={UI.bindTaroUI(this, 'userInfo.signature')}
        />
        <AtInput
          name="value"
          title="邮箱"
          type="text"
          placeholder="请输入邮箱"
          value={userInfo.email}
          onChange={UI.bindTaroUI(this, 'userInfo.email')}
        />
        <AtButton size="small" className="main-button" formType="submit">提交</AtButton>
      </AtForm>
    </AppPageLayout>)
  }
}

export default UserDetails as ComponentClass<PageOwnProps, PageState>
