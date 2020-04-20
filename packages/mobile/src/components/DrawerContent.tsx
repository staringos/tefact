import { ComponentClass } from 'react'
import Taro, { Component } from '@tarojs/taro'
import { View, Text } from '@tarojs/components'
import { connect } from '@tarojs/redux'
import { AtButton, AtListItem, AtList } from 'taro-ui'

import { Org } from '@arrplat/common'
import '../assets/styles/components/drawer-content.scss'

import { setCurrentOrg } from '../actions/org'
import { openDialog } from '../actions/system'
import { DIALOGS } from '../constants/system'

type PageStateProps = {
  currentOrgId: string,
  orgs: Org[],
}
type PageDispatchProps = {
  onSetCurrentOrg: (id: string) => any,
  onOpenDialog: ({ key, value }) => any,
}
type PageOwnProps = {
  title?: string | undefined,
  onLeftClick?: () => any | undefined,
}
type PageState = {}
type IProps = PageStateProps & PageDispatchProps & PageOwnProps

interface PageHeader {
  props: IProps
}

@connect(({ org }) => ({
  currentOrgId: org.currentOrgId,
  orgs: org.orgs,
}), (dispatch) => ({
  onSetCurrentOrg: setCurrentOrg(dispatch),
  onOpenDialog: openDialog(dispatch),
}))
class PageHeader extends Component {

  public switchCurrentOrg = (id) => {
    const { onSetCurrentOrg } = this.props
    onSetCurrentOrg(id)
  }

  public handleOpenOrgDialog = () => {
    const { onOpenDialog } = this.props
    onOpenDialog({ key: DIALOGS.ORG_MODIFY_DIALOG, value: true })
  }

  public render() {
    const { currentOrgId, orgs } = this.props
    const res = Taro.getSystemInfoSync()

    return (
      <View className="drawer-content" style={`padding-top: ${res.statusBarHeight}px`}>
        <View className="title-wrapper">
          <Text className="title">我的组织</Text>
        </View>
        <AtList>
          {orgs && orgs.map((org, i) => (
            <AtListItem
              customStyle={{backgroundColor: '#333'}}
              extraText={org.id === currentOrgId ? "✔️" : ""}
              title={org.name}
              thumb={org.head_url}
              key={i}
              onClick={() => this.switchCurrentOrg(org.id)}
            />
          ))}
        </AtList>
        <View className="drawer-bottom">
          <AtButton type="primary" size="small" onClick={this.handleOpenOrgDialog}>创建组织</AtButton>
        </View>
      </View>
    )
  }
}

export default PageHeader as ComponentClass<PageOwnProps, PageState>
