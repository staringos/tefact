import { View, Text, Image } from '@tarojs/components'
import Taro, { Component } from '@tarojs/taro'
import { connect } from '@tarojs/redux'
import { ComponentClass } from 'react'
import { User, Org } from '@arrplat/common'
import { AtList, AtListItem, AtModal } from 'taro-ui'

import ArrIcon from '../../components/ui/ArrIcon'
import '../../assets/styles/pages/user.scss'
import ShareToolbar from '../../components/ShareToolbar'
import wechatIcon from '../../assets/icon/wechat.png'
import mobileIcon from '../../assets/icon/mobile.png'
import { currentOrgGetter } from '../../actions/org'
import { logout } from '../../actions/system'
import OrgBar from '../../components/OrgBar'
import Layout from '../../layout'

import Config = Taro.Config

type PageStateProps = {
  user: User,
  currentOrg: Org
}
type PageDispatchProps = {
  onLogout: any
}
type PageOwnProps = {}
type PageState = {
  isOpened: boolean
}
type IProps = PageStateProps & PageDispatchProps & PageOwnProps

interface UserPage {
  props: IProps
}

@connect(({ user, org }) => ({
  user: user.user,
  currentOrg: currentOrgGetter(org)
}), (dispatch) => ({
  onLogout: logout(dispatch)
}))
class UserPage extends Component {

  public state = {
    isOpened: false
  }

  public config: Config = {
    navigationBarTitleText: '我的',
  }

  public onShareAppMessage() {
    const { user, currentOrg } = this.props

    return {
      title: `[微信名片] ${currentOrg.name} - ${user.nickname}`,
      path: `pages/apps/card/User?id=${user.id}`,
      imageUrl: '',
      success: (res) => {
        // TODO Data analysis
        console.log('success:', res)
      },
      fail: () => {
        console.log('转发失败')
      }
    }
  }

  public handleSetting = () => {
    console.log('handleSetting handleSetting')
    Taro.navigateTo({ url: '/pages/user/userDetails' })
  }

  public handleLogout = () => {
    this.setState({ isOpened: true })
  }

  public handleConfirm = () => {
    this.props.onLogout()
    this.setState({ isOpened: false })
    Taro.redirectTo({ url: '/pages/auth/index' })
  }

  public handleCancel = () => {
    this.setState({ isOpened: false })
  }

  public render() {
    const { user, currentOrg } = this.props
    const { isOpened } = this.state

    if (!user || !currentOrg) return (<View />)

    return (
      <Layout title={this.config.navigationBarTitleText} className="page user-page">
        <View className="user-card">
          <View className="avatar-wrapper">
            <Image className="avatar" src={user.head_url} />
          </View>
          <View className="details">
            <View className="row">
              <Text className="title">{user.nickname} </Text>
              <Text className="second-title">{currentOrg.staff_info.job_title}</Text>
            </View>
            <Text className="stand-text">{user.signature}</Text>
            <View className="more-info">
              <ArrIcon size={26} src={mobileIcon} />
              <Text className="details-item-value">{user.phone}</Text>
              {user.weChatNumber && (
                <ArrIcon size={26} src={wechatIcon} />
              )}
              <Text className="details-item-value">{user.weChatNumber}</Text>
            </View>
          </View>
          <ShareToolbar onSetting={this.handleSetting} />
        </View>
        <OrgBar org={currentOrg} />
        <View className="space">
          <AtList>
            <AtListItem title="使用手册" arrow="right" />
            <AtListItem title="意见反馈" arrow="right" />
            <AtListItem title="退出登录" onClick={this.handleLogout} />
          </AtList>
        </View>

        <AtModal
          isOpened={isOpened}
          title="退出"
          cancelText="取消"
          confirmText="确认"
          onCancel={this.handleCancel}
          onConfirm={this.handleConfirm}
          content="确定退出账号吗"
        />
      </Layout>
    )
  }
}

export default UserPage as ComponentClass<PageOwnProps, PageState>
