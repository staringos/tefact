import Taro from '@tarojs/taro'
import IndexComponent from '../../../components/apps/org/index'

import AppPageLayout from '../../../layout/AppPageLayout'

const Index = () => (
  <AppPageLayout title="组织基本信息" className="org-page" hasBack>
    <IndexComponent />
  </AppPageLayout>
)

export default Index
