import Taro from '@tarojs/taro'
import { View, Button } from '@tarojs/components'

import ArrIcon from './ui/ArrIcon'
import shareIcon from '../assets/icon/lingcunwei.png'
import settingIcon from '../assets/icon/shezhi.png'
import '../assets/styles/components/share-toolbar.scss'

const ShareToolbar = ({ onSetting }) => (
  <View className="share-toolbar flex1">
    <Button className="share-btn-wrapper" openType="share">
      <ArrIcon src={shareIcon} />
    </Button>
    <Button className="share-btn-wrapper" onClick={onSetting} >
      <ArrIcon src={settingIcon} />
    </Button>
  </View>
)

export default ShareToolbar
