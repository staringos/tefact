import Taro, { Component } from '@tarojs/taro'
import { View } from '@tarojs/components'

import '../assets/styles/layout.scss'
import Header from '../components/Header'
import OrgModifyDialog from '../components/OrgModifyDialog'

interface Props {
  children: any
  className?: string | undefined
  hasBack?: boolean | undefined
  title?: string | undefined
}

interface State {
  showDrawer: boolean
}

class AppPageLayout extends Component<Props, State> {

  // eslint-disable-next-line react/sort-comp
  public static options = {
    addGlobalClass: true,
  }

  public render() {
    const { title, className, children, hasBack } = this.props

    return (
      <View className="page-layout">
        <Header title={title} hasBack={hasBack} hideOrgIcon />
        <View className={`page-container page ${className}`}>
          {children}
        </View>
        <OrgModifyDialog />
      </View>
    )
  }
}

export default AppPageLayout
