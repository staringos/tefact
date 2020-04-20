import Taro from '@tarojs/taro'
import { Image } from '@tarojs/components'
import '../assets/styles/components/avatar.scss'

interface Props {
  src: any
  length?: number | string
}

const Avatar = (props: Props) => {
  const { src, length } = props
  const styles = {} as any

  styles.width = (length || 120) + 'px'
  styles.height = (length || 120) + 'px'

  return (
    <Image className="arr-avatar" style={styles} src={src} />
  )
}

export default Avatar
