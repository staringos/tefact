import { Image, View } from '@tarojs/components'
import Taro from '@tarojs/taro'
import '../assets/styles/components/card.scss'

interface Props {
  children: any
  backgroundColor?: string
  backgroundImage?: string
  style?: any
  className?: string
}

const Card = (prop: Props) => {
  const { className, backgroundColor, backgroundImage, children, style } = prop
  const viewStyle = backgroundColor ? { ...style, 'background-color': backgroundColor } : style

  return (
    <View className={'card-component ' + className} style={viewStyle}>
      {backgroundImage && <Image className="bg-image" src={backgroundImage} />}
      <View className="card-container">
        {children}
      </View>
    </View>)
}

export default Card
