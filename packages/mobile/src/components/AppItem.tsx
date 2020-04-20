import Taro, { Component } from '@tarojs/taro'
import { View, Text, Image } from '@tarojs/components'
import { Application } from '@arrplat/common'

import '../assets/styles/components/app-item.scss'

interface Props {
  app: Application,
  currentId?: string | undefined,
  icon?: string | undefined,
  onClick?: (app: Application) => any,
}

class AppItem extends Component<Props> {
  public static options = {
    addGlobalClass: true,
  }

  public handleToDetails(e) {
    e.stopPropagation()
    const { app } = this.props

    Taro.navigateTo({ url: `/pages/apps/org/appDetails?app=${JSON.stringify(app)}` })
  }

  public render() {
    const { app, currentId, onClick, icon } = this.props

    return (<View
      className={`app-item ${currentId === app.id ? 'active' : ''}`}
      onClick={this.handleToDetails}
    >
      <View className={`content ${currentId === app.id ? 'active' : ''}`}>
        <View className="checkbox" onClick={(e) => { e.stopPropagation(); onClick && onClick(app) }}>
          <View className={`at-icon ${icon ? icon : 'at-icon-check'}`} />
        </View>
        <Image src={app.icon} className="app-icon" />
      </View>
      <View className="footer">
        <Text className="app-name">{app.title}</Text>
        <View className="at-icon at-icon-arrow-right" />
      </View>
    </View>)
  }
}

export default AppItem
