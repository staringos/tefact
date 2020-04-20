import { ComponentClass } from 'react'
import Taro, { Component } from '@tarojs/taro'
import { View, Text } from '@tarojs/components'
import { connect } from '@tarojs/redux'
import { Org } from '@arrplat/common'
import { AtAvatar, AtIcon } from 'taro-ui'
import '../assets/styles/components/header.scss'

import { currentOrgGetter } from '../actions/org'

type PageStateProps = {
  currentOrg: Org,
}
type PageDispatchProps = {}
type PageOwnProps = {
  title?: string | undefined,
  onLeftClick?: () => any | undefined,
  hasBack?: boolean | undefined,
  hideOrgIcon?: boolean | undefined,
}
type PageState = {}
type IProps = PageStateProps & PageDispatchProps & PageOwnProps

interface PageHeader {
  props: IProps
}

@connect(({ org }) => ({
  currentOrg: currentOrgGetter(org)
}))
class PageHeader extends Component {
  // eslint-disable-next-line react/sort-comp
  public static options = {
    addGlobalClass: true,
  }

  public handleLeftClick = () => {
    const { onLeftClick, hasBack } = this.props
    if (onLeftClick) {
      onLeftClick()
    }

    if (hasBack) {
      Taro.navigateBack()
    }
  }

  public render() {
    const { currentOrg, title, hasBack, hideOrgIcon } = this.props
    const res = Taro.getSystemInfoSync()

    if (!currentOrg) {
      return (<View />)
    }

    return (
      <View className="page-header" style={`margin-top: ${res.statusBarHeight}px`}>
        <View className="open-drawer" onClick={this.handleLeftClick}>
          {!hideOrgIcon && <AtAvatar circle image={currentOrg.head_url} size="small" />}
          {hasBack && <AtIcon value="chevron-left" size="20"></AtIcon>}
        </View>
        <Text className="page-header-title">
          {title}
        </Text>
      </View>
    )
  }
}

export default PageHeader as ComponentClass<PageOwnProps, PageState>
