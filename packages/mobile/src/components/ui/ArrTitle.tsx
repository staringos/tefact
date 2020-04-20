import Taro from '@tarojs/taro'
import { View, Text } from '@tarojs/components'
import '../../assets/styles/components/arr-title.scss'

const ArrTitle = ({ children }) => (<View className="arr-title">
  <Text className="text">{children}</Text>
</View>)

export default ArrTitle
