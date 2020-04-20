import { ComponentClass } from 'react'
import Taro, { Component } from '@tarojs/taro'
import { connect } from '@tarojs/redux'
import { AtModal, AtModalHeader } from 'taro-ui'

import '../assets/styles/components/home-header.scss'
import { closeDialog } from '../actions/system'

type PageStateProps = {
  dialogsVisible: any[],
}

type PageDispatchProps = {
  onCloseDialog: (key: string) => any,
}

type PageOwnProps = {
  children: any,
  title: string,
  key: string,
}
type PageState = {}

type IProps = PageStateProps & PageDispatchProps & PageOwnProps

interface Dialog {
  props: IProps
  state: PageState
}

@connect(({ system }) => ({
  dialogsVisible: system.dialogsVisible,
}), (dispatch) => ({
  onCloseDialog: closeDialog(dispatch),
}))
class Dialog extends Component {

  constructor(props) {
    super(props)
  }

  public handleClose = (item) => {
    this.props.onCloseDialog(item.id)
  }

  public render() {
    const { children, title, dialogsVisible, key } = this.props

    return (
      <AtModal
        isOpened={!!dialogsVisible[key]}
        onClose={this.handleClose}
      >
        {title && (<AtModalHeader>{title}</AtModalHeader>)}
        {children}
      </AtModal>
    )
  }
}

export default Dialog as ComponentClass<PageOwnProps, PageState>
