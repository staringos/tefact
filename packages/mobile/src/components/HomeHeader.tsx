import { ComponentClass } from 'react'
import Taro, { Component } from '@tarojs/taro'
import { AtAvatar } from 'taro-ui'
import { View, Text } from '@tarojs/components'
import { User, Application } from '@arrplat/common'
import { connect } from '@tarojs/redux'

import ArrMenuIcon from '../components/ui/ArrMenuIcon'
import Tab from '../components/Tab'
import '../assets/styles/components/home-header.scss'
import { setCurrentApp, currentAppGetter } from '../actions/app'

type PageStateProps = {
  currentApp: Application
  user: User
  apps: Application[],
}

type PageDispatchProps = {
  onSetCurrentApp: (id: string) => any,
}

type PageOwnProps = {}
type PageState = {
  current: any,
}

type IProps = PageStateProps & PageDispatchProps & PageOwnProps

interface HomeHeader {
  props: IProps
  state: PageState
}

@connect(({ user, app }) => ({
  user: user.user,
  apps: app.apps,
  currentApp: currentAppGetter(app),
}), (dispatch) => ({
  onSetCurrentApp: setCurrentApp(dispatch),
}))
class HomeHeader extends Component {

  constructor(props) {
    super(props)
  }

  // eslint-disable-next-line react/sort-comp
  public static options = {
    addGlobalClass: true,
  }

  public handleSwitch = (item) => {
    this.props.onSetCurrentApp(item.id)
  }

  public render() {
    const { user, apps, currentApp } = this.props
    const activeId = currentApp ? currentApp.id : null

    return (
      <View className="home-header">
        <View className="background" />
        <View className="welcome">
          <Text className="text">Hello, {user.nickname}</Text>
          <View onClick={() => Taro.switchTab({ url: '/pages/user/index' })}>
            <AtAvatar className="avatar" image={user.head_url} circle size="small" />
          </View>
        </View>
        <View className="card">
          <Tab items={apps} color="white" activeId={activeId} onSwitch={this.handleSwitch} />
          <View className="menu-list">
            {currentApp && currentApp.menus.map((menu, i) => (
              <ArrMenuIcon key={i} app={menu} adminRoute={currentApp.admin_route} />
            ))}
          </View>
        </View>
      </View>
    )
  }
}

export default HomeHeader as ComponentClass<PageOwnProps, PageState>
