import Taro, { Component } from '@tarojs/taro'
import { View } from '@tarojs/components'
import { AtDrawer } from 'taro-ui'

import '../assets/styles/layout.scss'
import Header from '../components/Header'
import DrawerContent from '../components/DrawerContent'
import OrgModifyDialog from '../components/OrgModifyDialog'

interface Props {
  children: any
  className: string
  title?: string | undefined
}

interface State {
  showDrawer: boolean
}

class Layout extends Component<Props, State> {

  // eslint-disable-next-line react/sort-comp
  public static options = {
    addGlobalClass: true,
  }

  public state = {
    showDrawer: false,
  }

  public handleLeftClick = () => {
    this.setState({ showDrawer: true })
  }

  public handleClose = () => {
    this.setState({ showDrawer: false })
  }

  public render() {
    const { title, className, children } = this.props
    const { showDrawer } = this.state

    return (
      <View className="page-layout">
        <Header title={title} onLeftClick={this.handleLeftClick} />
        <AtDrawer
          show={showDrawer}
          mask
          onClose={this.handleClose}
        >
          <DrawerContent />
        </AtDrawer>
        <View className={`page-container page ${className}`}>
          {children}
        </View>
        <OrgModifyDialog />
      </View>
    )
  }
}

export default Layout
