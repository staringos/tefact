import Taro from '@tarojs/taro'
import { Text, View } from '@tarojs/components'
import { AtAvatar, AtButton} from 'taro-ui'

import '../assets/styles/components/org-bar.scss'

interface Props {
  org: any
}

const OrgBar = ({ org }: Props) => (
  <View className="org-bar flex-center">
    {org && (
      <View className="avatar-area">
        <AtAvatar size="small" circle image={org.head_url} />
        <View style="line-height: 55px;">
          <Text className="org-name">{org.name}</Text>
        </View>
      </View>
    )}
    <AtButton type="primary" size="small">查看详情</AtButton>
  </View>
)

export default OrgBar
