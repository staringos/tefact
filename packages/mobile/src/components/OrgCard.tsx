import { Text, View } from '@tarojs/components'
import Taro from '@tarojs/taro'
import { Org } from '@arrplat/common'
import Card from './Card'
import Avatar from './Avatar'
import '../assets/styles/components/org-card.scss'
import ShareToolbar from './ShareToolbar'

interface Props {
  org: Org
}

const handleSetting = () => {
  Taro.navigateTo({ url: '/pages/apps/org/index' })
}

const OrgCard = ({ org }: Props) => {
  if (!org) return (<View />)

  return (
    <View className="org-card-wrapper">
      <Card>
        <View className="org-card-container">
          <View className="avatar-wrapper flex-center">
            <Avatar length="67" src={org.head_url} />
          </View>
          <View className="details">
            <Text className="title">{org.name}</Text>
            {org.description && (<Text className="details-item">简 介: {org.description}</Text>)}
            {org.website && (<Text className="details-item">官 网: {org.website}</Text>)}
            {org.address && (<Text className="details-item">地 址: {org.address}</Text>)}
          </View>
          <ShareToolbar onSetting={handleSetting} />
        </View>
      </Card>
    </View>)
}

export default OrgCard
