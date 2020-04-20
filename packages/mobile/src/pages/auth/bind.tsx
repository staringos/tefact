import { ComponentClass } from 'react'
import Taro, { Component } from '@tarojs/taro'
import { View, Button, Text, Input, Image } from '@tarojs/components'
import { connect } from '@tarojs/redux'
import '../../assets/styles/pages/bind.scss'
import { bindAccount } from '../../actions/auth'
import { service, UI } from '../../utils'


type PageOwnProps = {
}

type PageState = {
  phone: string,
  password: string,
  verify_code: string,
  uuid: string,
  verifyImageUrl: string,
}

type PageDispatchProps = {
  onBindAccount: any
  hasLogin: any
}

type IProps = PageDispatchProps & PageOwnProps

interface Bind {
  props: IProps
  state: PageState
}

const mapDispatchToProps = (dispatch) => ({
  onBindAccount: bindAccount(dispatch)
})

@connect(()  => ({}), mapDispatchToProps)
class Bind extends Component {

  constructor(props) {
    super(props)

    this.state = {
      phone: '',
      password: '',
      verify_code: '',
      uuid: '',
      verifyImageUrl: '',
    }
  }

  public async componentDidMount() {
    console.log('did mounted 1')
    await this.refreshVerify()
  }

  public refreshVerify = async () => {
    const res = await service.auth.verifyImage()
    const data = res.data.data
    this.setState({
      uuid: data.uuid,
      verifyImageUrl: `data:image/jpeg;base64,${data.verify_code_image}`,
    })
  }

  public handleBindAccount = () => {
    const params = {
      phone: this.state.phone,
      password: this.state.password,
      uuid: this.state.uuid,
      verify_code: this.state.verify_code
    }

    if (!params.phone || params.phone.length < 1 || !params.password || params.password.length < 1) {
      return Taro.showToast({ title: '请填写正确的手机号或密码', icon: 'none', duration: 2000 })
    }

    const { onBindAccount } = this.props

    onBindAccount(params).then(() => {
      Taro.showToast({ title: '绑定成功!', icon: 'success', duration: 2000 })
      Taro.switchTab({ url: '/pages/index/index' })
    }).catch(e => {
      e.message && Taro.showToast({ title: e.message, icon: 'none', duration: 2000 })
      this.refreshVerify()
    })
  }

  public render() {
    const { phone, password, verifyImageUrl, verify_code } = this.state

    const phoneBind = UI.bind(this, 'phone')
    const passwordBind = UI.bind(this, 'password')
    const verifyBind = UI.bind(this, 'verify_code')

    return (
      <View className="page-container bind-page flex-center">
        <View className="bind-form">
          <Text className="title">绑定账号</Text>
          <View className="input-area">
            <View className="input">
              <Input type="text" value={phone} onInput={phoneBind} placeholder="请输入手机号" focus />
            </View>
            <View className="input">
              <Input password value={password} onInput={passwordBind} placeholder="请输入密码" focus />
            </View>
            <View className="input verify-code">
              <Input type="text" value={verify_code} onInput={verifyBind} placeholder="请输入验证码" focus />
              <Image onClick={this.refreshVerify} className="verify-image" src={verifyImageUrl} />
            </View>
            <Button className="button button-round button-primary bind-button" onClick={this.handleBindAccount}>
              微信登录
            </Button>
          </View>
        </View>
      </View>
    )
  }
}

export default Bind as ComponentClass<PageOwnProps, PageState>
