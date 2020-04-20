import { Image, Text, View } from '@tarojs/components'
import Taro from '@tarojs/taro'
import { Menu } from '@arrplat/common'

import '../../assets/styles/components/menu-icon.scss'

interface Props {
  app: Menu
  adminRoute?: string | undefined
}

const ArrMenuIcon = ({ app, adminRoute }: Props) => {
  const handleClick = () => {
    adminRoute && Taro.navigateTo({ url: `/pages/apps/${adminRoute}/${app.link && app.link.length > 1 ? app.link : 'index'}` })
  }

  return (
    <View className="app-icon" onClick={handleClick}>
      <Image className="menu-image" src={app.icon} />
      <Text className="app-name">{app.title || app.name}</Text>
    </View>)
}

export default ArrMenuIcon
