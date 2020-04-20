import { ComponentClass } from 'react'
import Taro, { Component } from '@tarojs/taro'
import { View, Button, Image } from '@tarojs/components'
import '../../assets/styles/pages/index.scss'
import logoImage from '../../assets/images/logo.png'

type PageOwnProps = {}
type PageState = {}

class Index extends Component {

  public toLogin() {
    Taro.navigateTo({ url: '/pages/auth/Bind' })
  }

  public render() {
    return (
      <View className="page-container welcome-page">
        <View>
          <Image className="logo" src={logoImage} />
        </View>
        <Button className="login-button" onClick={this.toLogin}>微信登录</Button>
      </View>
    )
  }
}

export default Index as ComponentClass<PageOwnProps, PageState>
