import { ComponentClass } from 'react'
import Taro from '@tarojs/taro'
import { connect } from '@tarojs/redux'
import { Org, OrgParams } from '@arrplat/common'
import { AtButton, AtInput, AtModal, AtModalAction, AtModalContent, AtModalHeader } from 'taro-ui'
import { Button } from '@tarojs/components'

import AppPageLayout from '../../../layout/AppPageLayout'
import TreeSelect from '../../../components/ui/TreeSelect'
import { Ichild } from '../../../components/ui/Tree'
import { currentOrgGetter, getRoles, modifyRole, deleteRole } from '../../../actions/org'
import { UI } from '../../../utils'

type PageStateProps = {
  currentOrg: Org,
}

type PageDispatchProps = {
  getAllRoles: (id: string) => Promise<any>,
  toModifyRole: (params: OrgParams) => Promise<any>,
  toDeleteRole: (params) => Promise<any>,
}
type PageOwnProps = {}
type PageState = {
  data: Ichild[],
  modifyDialogVisible: boolean,
  roleName: string,
  currentRoleId: string | undefined,
}
type IProps = PageStateProps & PageDispatchProps & PageOwnProps

interface RulesPage {
  props: IProps
  state: PageState
}

@connect(({ org }) => ({
    currentOrg: currentOrgGetter(org),
  }),
  (dispatch) => ({
    getAllRoles: getRoles(dispatch),
    toModifyRole: modifyRole(dispatch),
    toDeleteRole: deleteRole(dispatch),
  }),
)
class RulesPage extends Taro.PureComponent {

  public state = {
    data: [] as Ichild[],
    modifyDialogVisible: false,
    roleName: '',
    currentRoleId: undefined,
  } as PageState

  public async componentDidMount() {
    const { currentOrg } = this.props

    if (currentOrg) await this.refreshData()
  }

  public static options = {
    styleIsolation: 'shared',
  }

  public refreshData = async () => {
    const { currentOrg, getAllRoles } = this.props
    const res = await getAllRoles(currentOrg.id)

    if (!res.data.data || res.data.data.length < 1) return

    const data = res.data.data.map(item => ({
      label: item.name,
      value: item.id,
      isLeaf: false,
      disabled: false,   // 是否禁用
      children: [],
    }))

    this.setState({
      data,
    })
  }

  public handleAdd = async () => {
    const { roleName, currentRoleId } = this.state
    const { toModifyRole, currentOrg } = this.props

    if (!roleName || roleName.length < 1)
      return Taro.showToast({ title: '请输入正确的角色名', icon: 'none' })

    const res = await toModifyRole({ orgId: currentOrg.id, roleName, roleId: currentRoleId })

    if (res.statusCode === 200) {
      Taro.showToast({title: '操作成功!'})
      this.setState({
        currentRoleId: undefined,
        roleName: '',
        modifyDialogVisible: false,
      })
      this.refreshData()
    } else {
      Taro.showToast({ title: res.data ? res.data.message : '操作失败!', icon: 'none' })
    }
  }

  public handleOpenDialog = (data) => {
    this.setState({
      currentRoleId: data ? data.value : undefined,
      roleName: data ? data.label : '',
      modifyDialogVisible: true,
    })
  }

  public handleDelete = (data) => {
    Taro.showModal({
      title: '角色删除',
      content: '确定要删除该角色吗？',
      showCancel: true,
      confirmText: '确定',
      cancelText: '取消',
    }).then(async (e) => {
      if (e.cancel) return

      const { toDeleteRole, currentOrg } = this.props
      const res = await toDeleteRole({ orgId: currentOrg.id, roleId: data.value })
      if (res.statusCode === 200) {
        Taro.showToast({title: '操作成功!'})
        this.refreshData()
      } else {
        Taro.showToast({ title: res.data ? res.data.message : '操作失败!', icon: 'none' })
      }
    })
  }

  public handleToDetails = (data) => {
    Taro.navigateTo({
      url: `/pages/apps/org/roleDetails?roleId=${data.value}&roleName=${data.label}`,
    })
  }

  public render() {
    const { data, modifyDialogVisible, roleName, currentRoleId } = this.state

    const rightComponent = [{
      icon: 'edit',
      onClick: this.handleOpenDialog,
    }, {
      icon: 'close',
      onClick: this.handleDelete,
    }]

    return (<AppPageLayout title="角色管理" hasBack>
      <AtButton type="primary" size="small" full={false} onClick={() => this.handleOpenDialog(null)}>添加角色</AtButton>
      <TreeSelect rightComponent={rightComponent} dataSource={data} onClick={this.handleToDetails} />

      <AtModal isOpened={modifyDialogVisible}>
        <AtModalHeader>{currentRoleId ? '增加' : '修改'}角色</AtModalHeader>
        <AtModalContent>
          <AtInput
            name="roleName"
            title="角色名"
            type="text"
            placeholder="请输入角色名"
            value={roleName}
            onChange={UI.bindTaroUI(this, 'roleName')}
          />
        </AtModalContent>
        <AtModalAction>
          <Button onClick={() => this.setState({ modifyDialogVisible: false })}>取消</Button>
          <Button onClick={this.handleAdd}>确定</Button>
        </AtModalAction>
      </AtModal>
    </AppPageLayout>)
  }
}

export default RulesPage as ComponentClass<PageOwnProps, PageState>
