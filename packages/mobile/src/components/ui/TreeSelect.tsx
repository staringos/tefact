import Taro from '@tarojs/taro'
import { View } from '@tarojs/components'
import cls from 'classnames'
import Tree, { ITree } from './Tree'
import '../../assets/styles/components/tree.scss'

const clsPrefix = 'cp-tree'

export default class TreeSelect extends Taro.PureComponent<ITree> {

  public static defaultProps = {
    multiple: false,
    dataSource: [],
    treeDefaultExpandAll: true,
    rightComponent: [],
    value: '',
    onClick: () => ({}),
    onChange: () => ({}),
  }

  public state = {
  }

  public static options = {
    styleIsolation: 'shared',
  }

  public render() {
    const {
      rightComponent, dataSource, multiple, value, onClick, onChange, treeDefaultExpandAll, loadData,
    } = this.props

    return (
      <View className={cls(clsPrefix, {
        [`${clsPrefix}-radio`]: !multiple,
        [`${clsPrefix}-multiple`]: multiple,
      })}
      >
        <Tree
          value={value}
          loadData={loadData}
          multiple={multiple}
          onChange={onChange}
          onClick={onClick}
          dataSource={dataSource}
          rightComponent={rightComponent}
          treeDefaultExpandAll={treeDefaultExpandAll}
        />
      </View>
    )
  }
}
