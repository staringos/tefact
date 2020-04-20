import { View } from '@tarojs/components'
import Taro, { Component, Config } from '@tarojs/taro'
import { connect } from '@tarojs/redux'
import { ComponentClass } from 'react'
import { Application, Org } from '@arrplat/common'

import { currentOrgGetter } from '../../actions/org'
import OrgCard from '../../components/OrgCard'
import ArrMenuIcon from '../../components/ui/ArrMenuIcon'
import ArrSection from '../../components/ui/ArrSection'
import ArrAppIcon from '../../components/ui/ArrAppIcon'
import '../../assets/styles/pages/org.scss'
import Layout from '../../layout'
import { setCurrentApp } from '../../actions/app'

type PageStateProps = {
  currentOrg: Org
  apps: Application[],
}

type PageDispatchProps = {
  toSetCurrentApp: (id) => any,
}
type PageOwnProps = {}
type PageState = {}
type IProps = PageStateProps & PageDispatchProps & PageOwnProps

interface OrgPage {
  props: IProps
}

@connect(({ org, app }) => ({
  currentOrg: currentOrgGetter(org),
  apps: app.apps,
}), (dispatch) => ({
  toSetCurrentApp: setCurrentApp(dispatch),
}))
class OrgPage extends Component {
  public config: Config = {
    navigationBarTitleText: '组织',
  }

  public onShareAppMessage() {
    const { currentOrg } = this.props

    return {
      title: `[微信名片] ${currentOrg.name} - ${currentOrg.description}`,
      path: `pages/apps/card/Org?id=${currentOrg.id}`,
      imageUrl: '',
      success: (res) => {
        // TODO Data analysis
        console.log('success:', res)
      },
      fail: () => {
        console.log('转发失败')
      },
    }
  }

  public handleAppClick = (app) => {
    const { toSetCurrentApp } = this.props
    toSetCurrentApp(app.id)
    Taro.switchTab({ url: `/pages/index/index?appId=${app.id}` })
  }

  public render() {
    const { currentOrg, apps } = this.props

    if (!apps || !currentOrg) return <View />

    const orgApp = apps.filter((app) => app.title === '组织管理')[0]

    return (
      <Layout title={this.config.navigationBarTitleText} className="org-page">
        <View className="flex-center">
          {currentOrg && (<OrgCard org={currentOrg} />)}
        </View>
        <ArrSection title="应用中心">
          {apps && apps.map((app, i) => <ArrAppIcon onClick={() => this.handleAppClick(app)} app={app} key={i} />)}
        </ArrSection>
        <ArrSection title="组织管理">
          {orgApp && orgApp.menus.map(
            (menu, e) => (<ArrMenuIcon adminRoute={orgApp.admin_route} app={menu} key={e} />))}
        </ArrSection>
      </Layout>
    )
  }
}

export default OrgPage as ComponentClass<PageOwnProps, PageState>
