import { ComponentClass } from 'react'
import Taro, { Component } from '@tarojs/taro'
import { Button } from '@tarojs/components'
import { AtModalContent, AtModalAction, AtInput } from 'taro-ui'
import { connect } from '@tarojs/redux'
import { OrgParams } from '@arrplat/common'

import { closeDialog } from '../actions/system'
import { UI } from '../utils'
import { DIALOGS } from '../constants/system'

import Dialog from './Dialog'
import { modifyOrg } from '../actions/org'

type PageStateProps = {
  dialogsVisible: any[],
}

type PageDispatchProps = {
  onCloseDialog: (key: string) => any,
  onModifyOrg: (data) => any,
}

type PageOwnProps = {}
type PageState = {
  formData: OrgParams,
}
type IProps = PageStateProps & PageDispatchProps & PageOwnProps

interface OrgModifyDialog {
  props: IProps
  state: PageState
}

@connect(({ system }) => ({
  dialogsVisible: system.dialogsVisible,
}), (dispatch) => ({
  onCloseDialog: closeDialog(dispatch),
  onModifyOrg: modifyOrg(dispatch),
}))
class OrgModifyDialog extends Component {

  public state = {
    formData: {
      name: '',
      unique_id: '',
      description: '',
    } as OrgParams,
  }

  public handleClose = () => {
    this.props.onCloseDialog(DIALOGS.ORG_MODIFY_DIALOG)
  }

  public handleSubmit = async () => {
    const res = await this.props.onModifyOrg(this.state.formData)
    if (res.statusCode === 200) {
      Taro.showToast({ title: `操作成功` })
      return this.handleClose()
    }

    if (res.data.message) {
      return Taro.showToast({ title: res.data.message, icon: 'none' })
    }

    Taro.showToast({ title: `请输入必填项`, icon: 'none' })
  }

  public render() {
    const { formData } = this.state

    return (
      <Dialog title="组织编辑" key={DIALOGS.ORG_MODIFY_DIALOG}>
        <AtModalContent>
          <AtInput
            name="name"
            title="组织名"
            type="text"
            placeholder="请输入组织名"
            value={formData.name}
            onChange={UI.bindTaroUI(this, 'formData.name')}
          />
          <AtInput
            name="unique_id"
            title="组织ID"
            type="text"
            placeholder="请输入组织ID"
            value={formData.unique_id}
            onChange={UI.bindTaroUI(this, 'formData.unique_id')}
          />
          <AtInput
            name="description"
            title="组织简介"
            type="text"
            placeholder="请输入组织简介"
            value={formData.description}
            onChange={UI.bindTaroUI(this, 'formData.description')}
          />
        </AtModalContent>
        <AtModalAction>
          <Button onClick={this.handleClose}>取消</Button>
          <Button onClick={this.handleSubmit}>确定</Button>
        </AtModalAction>
      </Dialog>
    )
  }
}

export default OrgModifyDialog as ComponentClass<PageOwnProps, PageState>
