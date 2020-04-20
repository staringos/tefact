import { ComponentClass } from 'react'
import Taro from '@tarojs/taro'
import { connect } from '@tarojs/redux'
import { View } from '@tarojs/components'
import { Application, Org } from '@arrplat/common'
import { AtButton } from 'taro-ui'
import { getSubtract } from '../../../utils'

import AppItem from '../../../components/AppItem'
import AppPageLayout from '../../../layout/AppPageLayout'
import { getAllApps, addApp, removeApp } from '../../../actions/app'
import { currentOrgGetter } from '../../../actions/org'
import '../../../assets/styles/pages/app.scss'
import ArrTitle from '../../../components/ui/ArrTitle'

type PageStateProps = {
  allApps: Application[],
  apps: Application[],
  currentOrg: Org,
}
type PageDispatchProps = {
  toGetAllApps: ({ orgId, isAll }) => Promise<any>,
  toAddApp: ({ orgId, appId }) => Promise<any>,
  toRemoveApp: ({ orgId, appId }) => Promise<any>,
}
type PageOwnProps = {}
type PageState = {
  currentAppId: string | undefined,
  uninstallApp: Application[],
}
type IProps = PageStateProps & PageDispatchProps & PageOwnProps

interface AppPage {
  props: IProps
  state: PageState
}

@connect(({ app, org }) => ({
    allApps: app.allApps,
    apps: app.apps,
    currentOrg: currentOrgGetter(org),
  }),
  (dispatch) => ({
    toGetAllApps: getAllApps(dispatch),
    toAddApp: addApp(dispatch),
    toRemoveApp: removeApp(dispatch),
  }),
)
class AppPage extends Taro.PureComponent {
  public state = {
    currentAppId: undefined,
  } as PageState

  public async componentWillMount() {
    await this.refreshData()
  }

  public componentWillReceiveProps(nextProps) {
    if (nextProps.apps !== this.props.apps || nextProps.allApps !== this.props.apps)
      this.compute(nextProps.apps, nextProps.allApps)
  }

  public compute(apps, allApps) {
    this.setState({
      uninstallApp: getSubtract(allApps, apps),
    })
  }

  public async refreshData() {
    const { currentOrg, toGetAllApps } = this.props
    if (!currentOrg) return

    await toGetAllApps({ orgId: currentOrg.id, isAll: 1 })
  }

  public handleAppClick = (app) => {
    this.setState({
      currentAppId: app.id,
    })
  }

  public handleRemoveApp = (app) => {
    const { currentOrg, toRemoveApp } = this.props

    if (app.deletable === 0) return Taro.showToast({ title: '该应用不能被删除!', icon: 'none' })

    Taro.showModal({
      title: '应用删除',
      content: '确定要删除该应用吗？',
      showCancel: true,
      confirmText: '确定',
      cancelText: '取消',
    }).then(async (e) => {
      if (e.cancel) return
      const res = await toRemoveApp({ orgId: currentOrg.id, appId: app.id })
      if (res.statusCode === 200) {
        this.setState({ currentAppId: undefined })
        return Taro.showToast({ title: '删除成功' })
      }

      return Taro.showToast({ title: res.data.message ? res.data.message : '删除失败', icon: 'none' })
    })
  }

  public handleAddApp = async () => {
    const { currentOrg, toAddApp } = this.props
    const { currentAppId } = this.state

    if (!currentAppId) return

    const res = await toAddApp({ orgId: currentOrg.id, appId: currentAppId })
    if (res.statusCode === 200) {
      this.setState({ currentAppId: undefined })
      return Taro.showToast({ title: '添加成功' })
    }

    return Taro.showToast({ title: res.data.message ? res.data.message : '添加失败' })
  }

  public render() {
    const { apps } = this.props
    const { currentAppId, uninstallApp } = this.state

    return (<AppPageLayout className="app-center" title="应用中心" hasBack>
      <ArrTitle>应用</ArrTitle>
      <View className="app-list">
        {uninstallApp && uninstallApp.map((item, i) => (
          <AppItem app={item} key={i} currentId={currentAppId} onClick={this.handleAppClick} />
        ))}
      </View>
      <ArrTitle>已添加应用</ArrTitle>
      <View className="app-list">
        {apps && apps.map((item, i) => (
          <AppItem icon="at-icon-close" app={item} key={i} currentId={currentAppId} onClick={this.handleRemoveApp} />
        ))}
      </View>
      {currentAppId && (<View className="app-footer">
        <AtButton className="main-button flex1" type="secondary" onClick={this.handleAddApp} full>添加</AtButton>
      </View>)}
    </AppPageLayout>)
  }
}

export default AppPage as ComponentClass<PageOwnProps, PageState>
