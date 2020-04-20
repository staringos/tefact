import { ComponentClass } from 'react'
import Taro from '@tarojs/taro'
import { Button } from '@tarojs/components'
import { connect } from '@tarojs/redux'
import { Org } from '@arrplat/common'

import { AtModal, AtModalContent, AtModalAction, AtModalHeader, AtInput } from 'taro-ui'
import AppPageLayout from '../../../layout/AppPageLayout'
import TreeSelect from '../../../components/ui/TreeSelect'
import { Ichild } from '../../../components/ui/Tree'
import { UI, loop } from '../../../utils'
import { currentOrgGetter, getAllDepartment, addDepartment, deleteDepartment, modifyDepartment } from '../../../actions/org'

type PageStateProps = {
  currentOrg: Org,
}

type PageDispatchProps = {
  getDepartments: (id) => Promise<any>,
  toAddDepartment: (params) => Promise<any>,
  toDeleteDepartment: (params) => Promise<any>,
  toModifyDepartment: (params) => Promise<any>,
}
type PageOwnProps = {}
type PageState = {
  data: Ichild[],
  modifyDialogVisible: boolean,
  isEdit: boolean,
  departmentName: string,
  currentDepartmentId: string | undefined,
}
type IProps = PageStateProps & PageDispatchProps & PageOwnProps

interface DepartmentPage {
  props: IProps
}

@connect(({ org }) => ({
    currentOrg: currentOrgGetter(org),
  }),
  (dispatch) => ({
    getDepartments: getAllDepartment(dispatch),
    toAddDepartment: addDepartment(dispatch),
    toModifyDepartment: modifyDepartment(dispatch),
    toDeleteDepartment: deleteDepartment(dispatch),
  }),
)
class DepartmentPage extends Taro.PureComponent {

  public state = {
    data: [] as Ichild[],
    modifyDialogVisible: false,
    departmentName: '',
    currentDepartmentId: undefined,
    isEdit: false,
  }

  public async componentWillMount() {
    const { currentOrg } = this.props
    if (currentOrg)
      await this.refreshData(currentOrg)
  }

  public async componentWillReceiveProps(nextProps) {
    if (nextProps.currentOrg !== this.props.currentOrg)
      await this.refreshData(nextProps.currentOrg)

    return true
  }

  public async refreshData(currentOrg) {
    const { getDepartments } = this.props

    if (!currentOrg) return

    const res = await getDepartments(currentOrg.id)

    if (res.statusCode !== 200 || res.data.data.langth < 0) return

    this.setState({
      data: loop(res.data.data),
    })
  }

  public handleDialogOpen = (params, isEdit = false) => {
    this.setState({
      modifyDialogVisible: true,
      currentDepartmentId: params.value,
      departmentName: isEdit ? params.label : '',
      isEdit,
    })
  }

  public handleAdd = async () => {
    const { departmentName, currentDepartmentId, isEdit } = this.state
    const { toAddDepartment, toModifyDepartment, currentOrg } = this.props

    if (!departmentName || departmentName.length < 1)
      return Taro.showToast({ title: '请输入部门名!', icon: 'none' })

    Taro.showLoading({ title: '加载中...' })

    const params = { orgId: currentOrg.id, departmentName } as any

    if (isEdit) params.id = currentDepartmentId
    else params.parentDepartmentId = currentDepartmentId

    const res = isEdit ? await toModifyDepartment(params) : await toAddDepartment(params)

    if (res.statusCode !== 200) {
      Taro.hideLoading()
      return Taro.showToast(res.data.message ? res.data.message : '操作失败!')
    }

    await this.refreshData(currentOrg)

    Taro.hideLoading()
    this.setState({
      modifyDialogVisible: false,
      departmentName: '',
    })
    Taro.showToast({ title: '操作成功!', icon: 'success' })
  }

  public handleDelete = (data) => {
    const { toDeleteDepartment, currentOrg } = this.props

    Taro.showModal({
      title: '部门删除',
      content: '确定要删除该部门吗？',
      showCancel: true,
      confirmText: '确定',
      cancelText: '取消',
    }).then(async (e) => {
      if (e.cancel) return

      const res = await toDeleteDepartment({ orgId: currentOrg.id, departmentId: data.value })
      if (res.statusCode === 200) {
        Taro.showToast({ title: '删除成功!', icon: 'success' })
        return this.refreshData(currentOrg)
      }

      Taro.showToast({ title: res.data.message ? res.data.message : '删除失败!', icon: 'none' })
    })
  }

  public handleToDetails = (id) => {
    console.log('handleToDetails id', id)
  }

  public render() {
    const { data, modifyDialogVisible, departmentName } = this.state

    const rightComponent = [{
      icon: 'add',
      onClick: this.handleDialogOpen,
    }, {
      icon: 'edit',
      onClick: (params) => this.handleDialogOpen(params, true),
    }, {
      icon: 'close',
      onClick: this.handleDelete,
    }]

    return (<AppPageLayout title="部门管理" hasBack>
      <TreeSelect
        value="fruit"
        dataSource={data}
        rightComponent={rightComponent}
        onChange={this.handleToDetails}
      />
      <AtModal isOpened={modifyDialogVisible}>
        <AtModalHeader>增加部门</AtModalHeader>
        <AtModalContent>
          <AtInput
            name="departmentName"
            title="部门名"
            type="text"
            placeholder="请输入部门名"
            value={departmentName}
            onChange={UI.bindTaroUI(this, 'departmentName')}
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

export default DepartmentPage as ComponentClass<PageOwnProps, PageState>
