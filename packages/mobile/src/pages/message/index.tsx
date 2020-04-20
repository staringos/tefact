import { ComponentClass } from 'react'
import Taro, { Config, Component } from "@tarojs/taro"
import { connect } from '@tarojs/redux'
import { Message } from '@arrplat/common'
import { AtList, AtListItem } from 'taro-ui'

import Layout from '../../layout'
import { setMessageAsRead } from '../../actions/user'

type PageStateProps = {
  messages: Message[],
}

type PageDispatchProps = {
  onMessageAsRead: (id: string) => any,
}
type PageOwnProps = {}
type PageState = {}
type IProps = PageStateProps & PageDispatchProps & PageOwnProps

interface MessagePage {
  props: IProps
}

@connect(({ user }) => ({
  messages: user.messages,
}), (dispatch) => ({
  onMessageAsRead: setMessageAsRead(dispatch),
}))
class MessagePage extends Component {
  public config: Config = {
    navigationBarTitleText: '组织',
  }

  public handleRead(id) {
    this.props.onMessageAsRead(id)
  }

  public render() {
    const { messages } = this.props

    return (
      <Layout title={this.config.navigationBarTitleText} className="index">
        <AtList>
          {
            messages && messages.map(msg => (
              <AtListItem
                key={msg.id}
                title={msg.title}
                note={msg.content}
                extraText={msg.is_read === 0 ? '⭕️' : ''}
                arrow="right"
                onClick={() => this.handleRead(msg.id)}
                thumb="http://img12.360buyimg.com/jdphoto/s72x72_jfs/t10660/330/203667368/1672/801735d7/59c85643N31e68303.png"
              />
            ))
          }
        </AtList>
      </Layout>)
  }
}

export default MessagePage as ComponentClass<PageOwnProps, PageState>
