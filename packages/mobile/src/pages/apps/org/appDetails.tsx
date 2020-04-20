import Taro from '@tarojs/taro'
import { View, Text, Image } from '@tarojs/components'
import { connect } from '@tarojs/redux'
import { Org, Application } from '@arrplat/common'
import { AtButton } from 'taro-ui'

import { addApp, removeApp } from '../../../actions/app'
import AppPageLayout from '../../../layout/AppPageLayout'
import { currentOrgGetter } from '../../../actions/org'
import '../../../assets/styles/pages/app-details.scss'

interface Props {
  toAddApp: ({ orgId, appId }) => any
  toRemoveApp: ({ orgId, appId }) => any
  apps: Application[]
  currentOrg: Org
}

interface State {
  app: Application
}

@connect(({ org, app }) => ({
  currentOrg: currentOrgGetter(org),
  apps: app.apps,
}), (dispatch) => ({
  toAddApp: addApp(dispatch),
  toRemoveApp: removeApp(dispatch),
}))
class AppDetails extends Taro.PureComponent<Props, State> {
  public async componentDidMount() {
    await this.refreshData()
  }

  public async refreshData() {
    const { apps } = this.props
    const { app } = this.$router.params
    const data = JSON.parse(app)
    data.status = apps.filter(item => item.id === data.id).length

    this.setState({
      app: data,
    })
  }

  public handleRemoveApp = () => {
    const { currentOrg, toRemoveApp } = this.props
    const { app } = this.state

    if (app.deletable === 0) return Taro.showToast({ title: '该应用不能被删除!', icon: 'none' })

    Taro.showModal({
      title: '应用移除',
      content: '确定要移除该应用吗？',
      showCancel: true,
      confirmText: '确定',
      cancelText: '取消',
    }).then(async (e) => {
      if (e.cancel) return
      Taro.showLoading({ title: '加载中...' })
      const res = await toRemoveApp({ orgId: currentOrg.id, appId: app.id })
      Taro.hideLoading()

      if (res.statusCode === 200) {
        this.refreshData()
        return Taro.showToast({ title: '删除成功' })
      }

      return Taro.showToast({ title: res.data.message ? res.data.message : '删除失败', icon: 'none' })
    })
  }

  public handleAddApp = async () => {
    const { currentOrg, toAddApp } = this.props
    const { app } = this.state

    Taro.showLoading({ title: '加载中...' })
    const res = await toAddApp({ orgId: currentOrg.id, appId: app.id })
    Taro.hideLoading()

    if (res.statusCode === 200) {
      this.refreshData()
      return Taro.showToast({ title: '添加成功' })
    }

    return Taro.showToast({ title: res.data.message ? res.data.message : '添加失败' })
  }

  public render() {
    const { app } = this.state
    if (!app) return (<View />)

    return (
      <AppPageLayout title="应用详情" className="app-details-page" hasBack>
        <View className="section">
          <View className="header">
            <Text className="title">{app.title}</Text>
            {app.status === 0
              && <AtButton className="option-button" onClick={this.handleAddApp} full={false} type="primary" size="small">添加应用</AtButton>}
            {app.status === 1
              && <AtButton className="option-button delete-button" onClick={this.handleRemoveApp} full={false} type="primary" size="small">移除应用</AtButton>}
          </View>
          <View className="profile-list">
            <View className="row">
              <View className="item">分 类：</View>
              <View>{app.application_category && app.application_category.name}</View>
            </View>
            <View className="row">
              <View className="item">最新版本：</View>
              <View>{app.version}</View>
            </View>
            <View className="row">
              <View className="item">添加次数：</View>
              <View>{app.install_number}</View>
            </View>
            <View className="row">
              <View className="item">上线时间：</View>
              <View>{app.create_time}</View>
            </View>
          </View>
        </View>
        <View className="section">
          <Text className="title">应用简介</Text>
          <Text>
            { app.description }
          </Text>
        </View>
        <View className="section">
          <Text className="title">应用图册</Text>
          <View>
            {app.images && app.images.map((image, i) => (<Image className="app-gallery-item" src={image} key={i} />))}
          </View>
        </View>
      </AppPageLayout>
    )
  }
}

export default AppDetails
