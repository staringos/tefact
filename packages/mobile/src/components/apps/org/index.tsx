import Taro, { Component } from '@tarojs/taro'
import { View } from '@tarojs/components'
import { Org } from '@arrplat/common'
import { connect } from '@tarojs/redux'
import { AtForm, AtInput, AtButton, AtAvatar } from 'taro-ui'
import { ComponentClass } from 'react'

import '../../../assets/styles/apps/org/index.scss'
import { currentOrgGetter, modifyOrg, getAllOrgs } from '../../../actions/org'
import { UI, imageUploadUrl } from '../../../utils'

type PageStateProps = {
  currentOrg: Org,
}

type PageDispatchProps = {
  toModifyOrg: (id) => Promise<any>,
  toGetAllOrgs: () => Promise<any>,
}
type PageOwnProps = {}
type PageState = {
}
type IProps = PageStateProps & PageDispatchProps & PageOwnProps

interface Index {
  props: IProps
}

@connect(({ org }) => ({
  currentOrg: currentOrgGetter(org),
}), (dispatch) => ({
  toModifyOrg: modifyOrg(dispatch),
  toGetAllOrgs: getAllOrgs(dispatch),
}))
class Index extends Component {
  public state = {
    org: {} as Org,
  }

  public componentWillMount() {
    this.refreshData()
  }

  public componentWillReceiveProps(nextProps): void {
    if (nextProps.currentProps !== this.props.currentOrg) this.refreshData()
  }

  public static options = {
    addGlobalClass: true,
  }

  public refreshData() {
    const { currentOrg } = this.props
    if (currentOrg) this.setState({ org: { ...currentOrg } })
  }

  public onSubmit = async () => {
    const { toModifyOrg, toGetAllOrgs } = this.props
    const { org } = this.state

    try {
      const res = await toModifyOrg(org)

      if (res.statusCode === 200)
        Taro.showToast({ title: '修改成功！' })

      toGetAllOrgs()
    } catch (e) {
      Taro.showToast({ title: '修改失败！' })
    }
  }

  public handleAvatarChanged = (e) => {
    console.log('e:', e)
  }

  public handleSelectImage = () => {
    Taro.chooseImage({
      sourceType: ['album', 'camera'],
      count: 1,
    }).then(async res => {
      if (res.tempFilePaths.length < 1) return

      const tmpUrl = res.tempFilePaths[0]
      const name = tmpUrl.substring(tmpUrl.lastIndexOf('/') + 1, tmpUrl.length)

      const uploadRes = await Taro.uploadFile({
        url: imageUploadUrl,
        filePath: tmpUrl,
        name,
      })

      console.log('handleSelectImage uploadRes:', uploadRes)

    })
  }

  public render() {
    const { org } = this.state

    return (<View className="org-page">
      <View className="card">
        <View onClick={this.handleSelectImage}>
          <AtAvatar circle size="large" image={org.head_url} />
        </View>
      </View>

      {/*<AtImagePicker*/}
      {/*  files={files}*/}
      {/*  onChange={this.handleAvatarChanged}*/}
      {/*/>*/}

      <AtForm
        onSubmit={this.onSubmit}
      >
        <AtInput
          name="name"
          title="组织名"
          type="text"
          placeholder="请输入组织名"
          value={org.name}
          onChange={UI.bindTaroUI(this, 'org.name')}
        />
        <AtInput
          name="value"
          title="简介"
          type="text"
          placeholder="请输入组织简介"
          value={org.description}
          onChange={UI.bindTaroUI(this, 'org.description')}
        />
        <AtInput
          name="value"
          title="官网"
          type="text"
          placeholder="请输入组织官网"
          value={org.website}
          onChange={UI.bindTaroUI(this, 'org.website')}
        />
        <AtInput
          name="value"
          title="地址"
          type="text"
          placeholder="请输入地址"
          value={org.address}
          onChange={UI.bindTaroUI(this, 'org.address')}
        />
        <AtButton size="normal" formType="submit">提交</AtButton>
      </AtForm>
    </View>)
  }
}

export default Index as ComponentClass<PageOwnProps, PageState>
