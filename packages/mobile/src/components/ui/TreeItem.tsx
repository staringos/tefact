import Taro from '@tarojs/taro'
import { View, Text } from '@tarojs/components'
import { AtCheckbox, AtIcon, AtAvatar } from 'taro-ui'
import cls from 'classnames'
import Tree from './Tree'

const iconSize = 20
const iconColor = '#C7C7CC'
const checkIconSize = 18
const checkIconColor = '#1890FF'

interface ITreeItem {
  [otherProps: string]: any
  rightComponent: any
}

interface ITreeItemState {
  visible: boolean
  loading: boolean
}

export default class TreeItem extends Taro.PureComponent<ITreeItem, ITreeItemState> {

  constructor(props) {
    super(props)
    const { treeDefaultExpandAll, data = {} } = props
    const { children } = data
    const visible = treeDefaultExpandAll && Array.isArray(children) && children.length > 0
    this.state = {
      visible,
      loading: false,
    }
  }

  public static options = {
    styleIsolation: 'shared',
  }

  public loaded = false

  public handleToggleMore = async () => {
    const { visible } = this.state
    const { data, loadData } = this.props
    const { children } = data
    const hasChild = Array.isArray(children) && children.length > 0
    if (hasChild || this.loaded) {
      this.setState({
        visible: !visible,
      })
      return
    }
    if (typeof loadData === 'function') {
      this.setState({loading: true})
      await loadData(data)
      return this.setState({
        visible: true,
        loading: false,
      }, () => {
        this.loaded = true
      })
    }

    this.setState({ visible: !visible })
  }

  public handleRadioTreeChange = (value, disabled) => {
    if (disabled) return
    const { onChange } = this.props
    onChange(value)
  }

  public render() {
    const { visible, loading } = this.state
    const {
      selectedValue, onChange, multiple, data, treeDefaultExpandAll, loadData, rightComponent, onClick,
    } = this.props

    const { label, children, value, isLeaf, disabled, thumb } = data || {}
    const moreIcon = loading ? 'loading-3' : visible ? 'chevron-down' : 'chevron-up'
    const isRenderLeafIcon = isLeaf || (Array.isArray(children) && children.length > 0)
    const checked = selectedValue === value

    return (
      <View className="tree-item" onClick={() => onClick(data)}>
        <View className="tree-item-content">
          {thumb && (
            <AtAvatar image={thumb} size="small" circle />
          )}
          {/* 多选树 */}
          {multiple && (
            <AtCheckbox
              options={[{
                label,
                value,
                disabled,
              }]}
              onChange={onChange}
              selectedList={selectedValue || []}
            />)}
          {/* 单选树 */}
          {!multiple && (
            <View
              onClick={() => this.handleRadioTreeChange(value, disabled)}
              className="tree-item-radio"
            >
              <Text className={cls('label', {checked, disabled})}>
                {label}
              </Text>
              {checked && (
                <AtIcon value="check" size={checkIconSize} color={checkIconColor} />
              )}
            </View>)}
          <View className="right-button-wrapper">
            {rightComponent && rightComponent.map((res, i) =>
              <View className={`right-button at-icon at-icon-${res.icon}`}
                key={i} onClick={(e) => { e.stopPropagation(); res.onClick(data) }}
              />)}
          </View>
          {/* 展开收起加载中状态下的图标 */}
          {isRenderLeafIcon && (
            <View className="tree-item-more" onClick={this.handleToggleMore}>
              <AtIcon value={moreIcon} size={iconSize} color={iconColor} />
            </View>)}
        </View>
        {/* 子级树 */}
        <View className={cls({
          none: !visible,
        })}
        >
          <Tree
            value={selectedValue}
            multiple={multiple}
            onChange={onChange}
            onClick={onClick}
            loadData={loadData}
            dataSource={children}
            treeDefaultExpandAll={treeDefaultExpandAll}
            rightComponent={rightComponent}
          />
        </View>
      </View>
    )
  }
}
