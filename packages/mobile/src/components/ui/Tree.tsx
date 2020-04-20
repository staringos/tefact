import Taro from '@tarojs/taro'
import { View } from '@tarojs/components'
import TreeItem from './TreeItem'

export interface Ichild {
  label: string,
  value: string | number,
  isLeaf?: boolean,
  children?: Ichild[],
}

export interface ITree {
  value: any
  onChange: (e) => any
  onClick: (e) => any
  dataSource: Ichild[]
  multiple?: boolean
  loadData?: () => any
  rightComponent?: any
  treeDefaultExpandAll?: boolean
}

export default class Tree extends Taro.PureComponent<ITree> {

  public state = {}

  public static options = {
    styleIsolation: 'shared',
  }

  public render() {
    const { rightComponent, dataSource, value: selectedValue,
      onChange, onClick, multiple, loadData, treeDefaultExpandAll } = this.props

    if (!Array.isArray(dataSource)) return null

    return (
      <View className="tree">
        {dataSource.map(item => {
          const { value } = item
          return (
            <TreeItem
              key={value}
              data={item}
              loadData={loadData}
              onClick={onClick}
              onChange={onChange}
              multiple={multiple}
              rightComponent={rightComponent}
              selectedValue={selectedValue}
              treeDefaultExpandAll={treeDefaultExpandAll}
            />
          )
        })}
      </View>
    )
  }
}
