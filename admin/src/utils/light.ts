import { Vue } from 'nuxt-property-decorator'
import cloneDeep from 'lodash/cloneDeep'

export const reorder = (list, i, position) => {
  if (position === 1 && i > 0) {
    const tmp = list[i]
    Vue.set(list, i, list[i - 1])
    Vue.set(list, i - 1, tmp)
  } else if  (position !== 1 && i < list.length - 1) {
    const tmp = list[i]
    Vue.set(list, i, list[i + 1])
    Vue.set(list, i + 1, tmp)
  }

  return list
}

/**
 * 在所有层级中查找对应的Menu
 * @param menus
 * @param target
 */
export const findMenu = async (menus, target) => {
  let currentIndex = -1
  let res = null as any
  await Promise.all(menus.map(async (menu, i) => {
    // 找到了 返回
    if (currentIndex !== -1 || res) return

    if (menu == target.menu)  // 当前层级找到对应节点
      currentIndex = i

    if (menu.children && menu.children.length > 0) {
      const value = await findMenu(menu.children, target) // 递归查找更深层级
      if (value) res = value
    }
  }))

  // 当前层级找到节点 返回值
  if (currentIndex !== -1)
    return { list: menus, index: currentIndex }

  // 如果是更深一层方法返回值 或者 默认值
  return res
}

/**
 * 递归查找需要修改层级菜单的父节点，做对应的修改
 * @param menus
 * @param target
 * @param newValue
 * @param type
 * @param flag add / modify / delete
 */
export const loopModify = async (menus, target, newValue: any = null , type = 'delete', flag = null) => {
  const value = await findMenu(menus, target)

  if (!value) return menus

  const { list, index } = value

  if (type === 'delete') list.splice(index, 1)
  if (type === 'modify') list[index] = newValue
  if (type === 'add')
    if (list[index].children) list[index].children.push(newValue)
    else list[index].children = [ newValue ]


  if (type === 'reorder')
    reorder(list, index, flag)

  return menus
}

export const loopChildren = (menus) => {
  const res = [] as any
  for (let i = 0; i < menus.length; i++) {
    const hasChildren = menus[i].children && menus[i].children.length > 0

    res.push({
      ...menus[i],
      menu: menus[i],
      children: hasChildren ? loopChildren(menus[i].children) : []
    })
  }
  return res
}

export const loopMenu = (menus) => {
  const flat = cloneDeep(menus)
  const root = [] as any
  flat.map(menu => {
    if (!menu.parent_id || menu.parent_id === "0") {
      if (!menu.children) menu.children = []
      root.push(menu)
      return
    }

    const parent = flat.filter(pre => pre.id === menu.parent_id)

    if (parent && parent.length > 0)
      if (parent[0].children)
        parent[0].children.push(menu)
      else
        parent[0].children = [menu]

  })

  return root;
}
