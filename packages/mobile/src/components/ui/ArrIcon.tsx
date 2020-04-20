import Taro from '@tarojs/taro'
import { Image } from '@tarojs/components'
import '../../assets/styles/components/arr-icon.scss'

interface Props {
  src?: any
  size?: number | undefined
  onClick?: ((event) => any) | undefined
}

const ArrIcon = ({ src, onClick, size }: Props) => (
  <Image
    onClick={onClick}
    style={size ? { width: Taro.pxTransform(size), height: Taro.pxTransform(size) } : {}}
    className="arr-icon" src={src}
  />
)

export default ArrIcon
