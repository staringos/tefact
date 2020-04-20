import { ComponentClass } from 'react'
import Taro from '@tarojs/taro'
import { connect } from '@tarojs/redux'
import { Text } from '@tarojs/components'
import { Org } from '@arrplat/common'
import { AtButton } from 'taro-ui'

import { currentOrgGetter, getRoleAuth, getAuth, saveRoleAuth } from '../../../actions/org'
import AppPageLayout from '../../../layout/AppPageLayout'
import ArrTitle from '../../../components/ui/ArrTitle'
import TreeSelect from '../../../components/ui/TreeSelect'
import { Ichild } from '../../../components/ui/Tree'

const loop = (data) => data ? data.map(item => {
  const isLeaf = !item.children || item.children.length < 1

  return ({
    label: item.name,
    value: item.id,
    isLeaf,
    disabled: false,   // 是否禁用
    children: isLeaf ? [] : loop(item.children),
  })
}) : []

type PageStateProps = {
  currentOrg: Org,
}
type PageDispatchProps = {
  toGetRoleAuth: (params) => Promise<any>,
  toGetAuth: (params) => Promise<any>,
  toSaveRoleAuth: (params) => Promise<any>,
}
type PageOwnProps = {
  roleId: string,
  roleName: string,
}
type PageState = {
  allAuth: Ichild[],
  authSelect: string[],
}
type IProps = PageStateProps & PageDispatchProps & PageOwnProps

interface RoleDetails {
  props: IProps
  state: PageState
}

@connect(({ org }) => ({
    currentOrg: currentOrgGetter(org),
  }),
  (dispatch) => ({
    toGetRoleAuth: getRoleAuth(dispatch),
    toGetAuth: getAuth(dispatch),
    toSaveRoleAuth: saveRoleAuth(dispatch),
  }),
)
class RoleDetails extends Taro.PureComponent {

  public state = {
    allAuth: [],
    authSelect: [],
  } as PageState

  public async componentWillMount() {
    await this.refreshData()
  }

  public refreshData = async () => {
    const { currentOrg, toGetRoleAuth, toGetAuth } = this.props
    const { roleId } = this.$router.params

    if (!currentOrg) return

    const resAuth = await toGetAuth(currentOrg.id)
    const res = await toGetRoleAuth({ orgId: currentOrg.id, roleId })

    if (res.statusCode !== 200) return
    const data = resAuth.data.data
    const allAuth = [ ...data.system_menu, ...data.application_menu ]

    this.setState({
      authSelect: res.data.data,
      allAuth: loop(allAuth),
    })
  }

  public handleSelect = (e) => {
    this.setState({
      authSelect: e,
    })
  }

  public handleSave = async () => {
    const { toSaveRoleAuth, currentOrg } = this.props
    const { authSelect } = this.state
    const { roleId } = this.$router.params

    const res = await toSaveRoleAuth({ roleId, orgId: currentOrg.id, auth: authSelect })

    if (res.statusCode === 200) {
      return Taro.showToast({ title: '修改成功！' })
    }

    Taro.showToast({ title: res.data.message ? res.data.message : '修改成功！' })
  }

  public render() {
    const { authSelect, allAuth } = this.state
    const { roleName } = this.$router.params

    return (<AppPageLayout hasBack title={roleName}>
      <ArrTitle>角色</ArrTitle>
      <Text>{roleName}</Text>
      <ArrTitle>权限列表</ArrTitle>
      <TreeSelect value={authSelect}
        multiple={true} dataSource={allAuth} onChange={this.handleSelect} />
      <AtButton type="primary" size="small" onClick={this.handleSave}>保存</AtButton>
    </AppPageLayout>)
  }
}

export default RoleDetails as ComponentClass<PageOwnProps, PageState>
