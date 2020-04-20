import Taro, { Component, Config } from '@tarojs/taro'
import { Provider } from '@tarojs/redux'
import 'taro-ui/dist/style/index.scss'

import Index from './pages/index'
import configStore from './store'
import { init } from './actions/system'
import './app.scss'

// 如果需要在 h5 环境中开启 React Devtools
// 取消以下注释：
// if (process.env.NODE_ENV !== 'production' && process.env.TARO_ENV === 'h5')  {
//   require('nerv-devtools')
// }

const store = configStore()
init(store.dispatch)()

class App extends Component {
  constructor(props) {
    super(props)
  }

  public config: Config = {
    pages: [
      // System
      'pages/index/index',
      'pages/user/index',
      'pages/user/userDetails',
      'pages/org/index',
      'pages/auth/bind',
      'pages/message/index',
      'pages/auth/index',

      // Wechat Card
      'pages/apps/card/user',
      'pages/apps/card/org',

      // Organization
      'pages/apps/org/app',
      'pages/apps/org/appDetails',
      'pages/apps/org/index',
      'pages/apps/org/rules',
      'pages/apps/org/department',
      'pages/apps/org/roleDetails',
      'pages/apps/org/staffs',
    ],
    window: {
      backgroundTextStyle: 'light',
      navigationBarBackgroundColor: '#fff',
      navigationBarTitleText: 'WeChat',
      navigationBarTextStyle: 'black',
      navigationStyle: 'custom',
    },
    tabBar: {
      color: '#999',
      selectedColor: '#3181DE',
      backgroundColor: '#fff',
      borderStyle: 'black',
      list: [{
        pagePath: 'pages/index/index',
        iconPath: './assets/icon/home.png',
        selectedIconPath: './assets/icon/home-active.png',
        text: '首页',
      }, {
        pagePath: 'pages/message/index',
        iconPath: './assets/icon/i-message.png',
        selectedIconPath: './assets/icon/i-message-active.png',
        text: '消息',
      }, {
        pagePath: 'pages/org/index',
        iconPath: './assets/icon/org.png',
        selectedIconPath: './assets/icon/org-active.png',
        text: '组织',
      }, {
        pagePath: 'pages/user/index',
        iconPath: './assets/icon/user.png',
        selectedIconPath: './assets/icon/user-active.png',
        text: '我的',
      }],
    },
  }

  public render() {
    return (
      <Provider store={store}>
        <Index />
      </Provider>
    )
  }
}

Taro.render(<App />, document.getElementById('app'))
