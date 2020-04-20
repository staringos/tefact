import Taro from '@tarojs/taro'
import { View, Text } from '@tarojs/components'
import '../../assets/styles/components/arr-section.scss'

interface Props {
  children: any,
  title?: string
}

const ArrSection = ({ children, title }: Props) => (
  <View className="arr-section">
    {title && (<Text className="title">{title}</Text>)}
    <View className="arr-section-container">
      {children}
    </View>
  </View>
)

export default ArrSection
