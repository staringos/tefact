import { ComponentClass } from 'react'
import Taro, { Component, Config } from '@tarojs/taro'
import { View } from '@tarojs/components'
import { connect } from '@tarojs/redux'
import { Application } from '@arrplat/common'

import HomeHeader from '../../components/HomeHeader'
import OrgIndex from '../../components/apps/org/index'
import { AuthStorage } from '../../utils'
import './index.scss'
import Layout from '../../layout'
import { currentAppGetter } from '../../actions/app'

type PageStateProps = {
  hasLogin: boolean,
  currentApp: Application,
}
type PageDispatchProps = {}
type PageOwnProps = {}
type PageState = {}
type IProps = PageStateProps & PageDispatchProps & PageOwnProps

interface Index {
  props: IProps
}

@connect(({ user, app }) => ({
  hasLogin: !!user.accessToken,
  currentApp: currentAppGetter(app),
}))
class Index extends Component {
  constructor(props) {
    super(props)

    if (!AuthStorage.getToken()) {
      Taro.redirectTo({ url: '/pages/auth/index' })
    }
  }

  public config: Config = {
    navigationBarTitleText: '首页',
  }

  // public getCurrentPage = () => {
  //   const { currentApp } = this.props
  //
  //   if (!currentApp) return null
  //
  //   try {
  //     const component = require(`../../components/apps/${currentApp.admin_route}/index.tsx`).default
  //     console.log('content:', component)
  //     return component
  //   } catch (e) {
  //     console.log('e:', e)
  //   }
  //   return null
  // }

  public render() {
    const { currentApp } = this.props

    if (!currentApp) return (<View />)

    return (
      <Layout title={this.config.navigationBarTitleText} className="index">
        <HomeHeader />
        { currentApp.admin_route === 'org' && <OrgIndex /> }
      </Layout>
    )
  }
}

export default Index as ComponentClass<PageOwnProps, PageState>
