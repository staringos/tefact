import { Image, Text, View } from '@tarojs/components'
import Taro from '@tarojs/taro'
import '../../assets/styles/components/app-icon.scss'

const ArrAppIcon = ({ app, onClick }) => (
  <View className="app-icon" onClick={onClick}>
    <Image className="app-image" src={app.icon} />
    <Text className="app-name">{app.title || app.name}</Text>
  </View>)

export default ArrAppIcon
