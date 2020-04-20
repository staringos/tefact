import { Text, View } from "@tarojs/components";
import Taro from "@tarojs/taro";
import '../assets/styles/components/tab.scss'

const Tab = ({ items, activeId, onSwitch, color }) => {
  const handleItemClick = (item) => {
    if (item.id !== activeId) onSwitch(item)
  }

  return (
    <View className="tab-list">
      {items && items.map((item, i) => (
        <View className="tab-item"  key={i} onClick={() => handleItemClick(item)}>
          <Text
            className={"tab-name" + (item.id === activeId ? " active" : "")}
            style={color ? `color: ${color};` : ''}
          >
            {item.title || item.name}</Text>
        </View>
      ))}
    </View>)
}

export default Tab
