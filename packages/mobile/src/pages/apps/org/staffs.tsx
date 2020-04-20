import { ComponentClass } from 'react'
import Taro from '@tarojs/taro'
import { Button, View, Picker } from '@tarojs/components'
import { connect } from '@tarojs/redux'
import { Org, Staff, Department, Role, DefaultStaff } from '@arrplat/common'

import { AtTag, AtCheckbox, AtButton, AtModal, AtModalContent, AtModalAction, AtModalHeader, AtInput } from 'taro-ui'
import AppPageLayout from '../../../layout/AppPageLayout'
import ArrTitle from '../../../components/ui/ArrTitle'
import { UI, loop } from '../../../utils'
import { currentOrgGetter, getAllStaffs, getAllDepartment, getRoles, addStaff, removeStaff } from '../../../actions/org'
import '../../../assets/styles/pages/staffs.scss'
import TreeSelect from '../../../components/ui/TreeSelect'

type PageStateProps = {
  currentOrg: Org,
}

type PageDispatchProps = {
  toGetAllStaffs: ({ orgId, departmentId }) => Promise<any>,
  toGetAllDepartment: ({ orgId, departmentId }) => Promise<any>,
  toGetAllRoles: ({ orgId }) => Promise<any>,
  toAddStaff: (staff: Staff) => Promise<any>,
  toRemoveStaff: ({ orgId, staffId }) => Promise<any>,
}
type PageOwnProps = {}
type PageState = {
  staff: Staff,
  staffs: Staff[],
  roles: Role[],
  departments: Department[],
  modifyDialogVisible: boolean,
  departmentDialogVisible: boolean,
  currentSuperior?: number,
  currentRoles: number[],
  currentDepartments: Department[],
}
type IProps = PageStateProps & PageDispatchProps & PageOwnProps

interface StaffsPage {
  props: IProps
  state: PageState
}

const defaultState = {
  staff: {} as Staff,
  currentDepartments: [],
  currentSuperior: undefined,
  currentRoles: [],
  modifyDialogVisible: false,
}

@connect(({ org }) => ({
    currentOrg: currentOrgGetter(org),
  }),
  (dispatch) => ({
    toGetAllStaffs: getAllStaffs(dispatch),
    toGetAllDepartment: getAllDepartment(dispatch),
    toGetAllRoles: getRoles(dispatch),
    toAddStaff: addStaff(dispatch),
    toRemoveStaff: removeStaff(dispatch),
  }),
)
class StaffsPage extends Taro.PureComponent {

  public state = {
    modifyDialogVisible: false,
    departmentDialogVisible: false,
    staff: { ...DefaultStaff } as Staff,
    staffs: [],
    roles: [],
    departments: [],
    selector: ['美国', '中国', '巴西', '日本'],
    selectorChecked: '',
    currentSuperior: undefined,
    currentRoles: [],
    currentDepartments: [],
  } as PageState

  public async componentDidMount() {
    await this.refreshData()
    this.refreshFormData()
  }

  public refreshFormData = async () => {
    const { toGetAllDepartment, toGetAllRoles, currentOrg } = this.props
    const resRoles = await toGetAllRoles(currentOrg.id)
    const resDepartment = await toGetAllDepartment(currentOrg.id)

    this.setState({
      roles: resRoles.statusCode === 200 ? resRoles.data.data : [],
      departments: resDepartment.statusCode === 200 ? resDepartment.data.data : [],
    })
  }

  public refreshData = async () => {
    const { currentOrg, toGetAllStaffs } = this.props
    if (!currentOrg) return

    const res = await toGetAllStaffs({ orgId: currentOrg.id, departmentId: -1 })

    if (res.statusCode === 200)
      this.setState({ staffs: res.data.data })
  }

  public handleInvite = async () => {
    const { currentOrg, toAddStaff } = this.props
    const { staffs, staff, currentDepartments, currentRoles, currentSuperior } = this.state

    const staffParams = {
      data: {
        ...staff,
        department_id_list: currentDepartments.map(item => item.id),
        superior_id: currentSuperior && staffs[currentSuperior].id,
        role_id_list: currentRoles,
      },
      orgId: currentOrg.id,
    }

    const res = await toAddStaff(staffParams)
    if (res.statusCode !== 200)
      return Taro.showToast({ title: res.data.message ? res.data.message : '操作失败', icon: 'none' })

    this.refreshData()
    this.setState({ ...defaultState })
    return Taro.showToast({ title: '操作成功' })
  }

  public handleOpenDialog = (params) => {
    const { staffs } = this.state
    let staffNew = { ...DefaultStaff }

    const data = params.data
    if (data && data.id) {
      staffNew = {
        ...staffNew,
        phone: data.user.phone,
        job_title: data.job_title,
        is_able: data.is_able,
      }

      let currentSuperior = undefined as any

      data.parent_superior && staffs.map((item, i) => {
        if (item.id === data.parent_superior.id) {
          currentSuperior = i
        }
      })

      this.setState({
        staff: staffNew,
        currentDepartments: data.org_department,
        currentSuperior,
        currentRoles: data.role.map(item => item.id),
      })
    }

    this.setState({
      modifyDialogVisible: true,
    })
  }

  public static options = {
    styleIsolation: 'shared',
  }

  public handlePickerChange = (key, e) => {
    this.setState({
      [key]: e.detail.value,
    })
  }

  public handleDepartmentSelect = async (e) => {
    const { departments } = this.state
    const currentDepartments = []
    const loopValue = async (data) => {
      if (!data) return

      await data.map(async (item) => {
        // @ts-ignore
        if (e.includes(item.id)) currentDepartments.push(item)

        if (item.child_org_departments)
          await loopValue(item.child_org_departments)
      })
    }

    await loopValue(departments)
    this.setState({ currentDepartments })
  }

  public handleDelete = async (e) => {
    const { currentOrg, toRemoveStaff } = this.props

    Taro.showModal({
      title: '成员移除',
      content: '确定要移除该成员吗？',
      showCancel: true,
      confirmText: '确定',
      cancelText: '取消',
    }).then(async (ee) => {
      if (ee.cancel) return

      const res = await toRemoveStaff({orgId: currentOrg.id, staffId: e.value})

      if (res.statusCode === 200) {
        this.refreshData()
        return Taro.showToast({title: '操作成功'})
      }

      Taro.showToast({title: res.data.message ? res.data.message : '操作失败'})
    })
  }

  public handleCancel() {
    this.setState({ ...defaultState })
  }

  public render() {
    const {
      currentDepartments, currentSuperior, currentRoles, modifyDialogVisible,
      staff, staffs, departmentDialogVisible, departments, roles,
    } = this.state

    const superiorData = currentSuperior || currentSuperior === 0 ? staffs[currentSuperior].user.nickname : []
    const rightComponent = [{
      icon: 'edit',
      onClick: (params) => this.handleOpenDialog(params),
    }, {
      icon: 'close',
      onClick: this.handleDelete,
    }]

    return (<AppPageLayout title="成员管理" className="staffs-page" hasBack>
      <AtButton className="main-button add-staff-button" onClick={this.handleOpenDialog} type="primary" size="small">
        添加成员
      </AtButton>
      <TreeSelect
        value="fruit"
        dataSource={staffs.map(item => ({
          value: item.id,
          label: item.user.nickname,
          isLeaf: true,
          disabled: false,   // 是否禁用
          children: [],
          data: item,
          thumb: item.user.user_info.head_url,
        }))}
        rightComponent={rightComponent}
        onChange={() => ({})}
      />
      <AtModal isOpened={modifyDialogVisible} closeOnClickOverlay={false} onCancel={this.handleCancel}>
        <AtModalHeader>邀请成员</AtModalHeader>
        <AtModalContent>
          <AtInput
            name="departmentName"
            title="手机号"
            type="text"
            placeholder="请输入成员手机号"
            value={staff.phone}
            onChange={UI.bindTaroUI(this, 'staff.phone')}
          />
          <AtInput
            name="job_title"
            title="岗位"
            type="text"
            placeholder="请输入成员岗位"
            value={staff.job_title}
            onChange={UI.bindTaroUI(this, 'staff.job_title')}
          />
          <View className="picker" onClick={() => this.setState({ departmentDialogVisible: true })}>
            部 门：{currentDepartments.map((item, i) => <AtTag key={i}>{item.name}</AtTag>)}
          </View>
          <Picker
            mode="selector"
            range={staffs.map(st => ({ ...st, nickname: st.user.nickname }))}
            onChange={(e) => this.handlePickerChange('currentSuperior', e)}
            value={currentSuperior || 0}
            range-key="nickname"
          >
            <View className="picker">
              直属上级：{superiorData}
            </View>
          </Picker>

          <ArrTitle>角色</ArrTitle>

          <AtCheckbox
            options={roles.map(item => ({ value: item.id, label: item.name }))}
            selectedList={currentRoles}
            onChange={(e) => { this.setState({ currentRoles: e })}}
          />
        </AtModalContent>
        <AtModalAction>
          <Button onClick={() => this.setState({ modifyDialogVisible: false })}>取消</Button>
          <Button onClick={this.handleInvite}>确定</Button>
        </AtModalAction>
      </AtModal>
      <AtModal
        isOpened={departmentDialogVisible}
        closeOnClickOverlay={false}
      >
        <AtModalHeader>选择部门</AtModalHeader>
        <AtModalContent>
          <TreeSelect
            onChange={this.handleDepartmentSelect}
            value={currentDepartments.map(item => item.id)}
            multiple
            dataSource={loop(departments)}
          />
        </AtModalContent>
        <AtModalAction>
          <Button onClick={() => this.setState({ departmentDialogVisible: false })}>
            确定
          </Button>
        </AtModalAction>
      </AtModal>
    </AppPageLayout>)
  }
}

export default StaffsPage as ComponentClass<PageOwnProps, PageState>
