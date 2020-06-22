const MenuType = [{
  key: 'customer',
  value: '自定义（链接 字段必填）',
}, {
  key: 'page',
  value: '配置页面（关联页面 字段必填）',
}]

const DefaultMenu = {
  application_id: null,
  name: '',
  link: '',
  type: 'customer',
  page_key: '',
}

const PageDirection = [{
  key: 'column',
  value: '纵向',
}, {
  key: 'row',
  value: '横向',
}]

const DefaultPage = {
  // key: '',
  title: '',
  direction: 'column',
  sections: [],
}

const DefaultPageSection = {
  title: '',
  entity_key: null,
  entity_params: null,
  type: 'list',
  has_add_btn: false,
}

const DefaultEntity = {
  key: null,
  table_name: null,
  data_type: 'db_table',
  sql: null,
  has_connect_org: true,
  fields: [],
}

const EntityFieldLinkType = [{
  key: 'button',
  value: '链接按钮',
}, {
  key: 'link',
  value: '链接地址',
}]

const DefaultEntityField = {
  is_primary: false,
  key: '',
  name: '',
  data_type: 'string',
  display_type: 'auto',
  type: 'value',
  iframe_url: null,
  sql: null,
  data_source_sql: null,
  dict_list: [],
  exists: ['list', 'details', 'modify'],
  buttons: [],
  link_address: null,
  has_link: false,
  link_button: null,
  has_sort: false,
  has_search: false,
  form_component: null,
  display_component: null,
  default_value: null,
  description: null,

  foreign_type: 'one-to-one',
  foreign_table_name: null,
  foreign_their_key: null,
  foreign_our_key: null,

  verify_pattern: null,
  verify_require: false,
  verify_only: false,
  verify_max: null,
  verify_min: null,
}

const ButtonType = [
  { key: 'edit', value: '修改' },
  { key: 'delete', value: '删除' },
  { key: 'details', value: '详情' },
  { key: 'add', value: '添加' },
  { key: 'link', value: '链接' },
  { key: 'action', value: '事件' },
  { key: 'dialog-details', value: '详情弹窗' },
  { key: 'dialog-list', value: '列表弹窗' },
]

const EntityFieldExists = [
  { key: 'details', value: '详情页' },
  { key: 'modify', value: '编辑页' },
  { key: 'list', value: '列表页' },
]

const EntityFieldType = [
  { key: 'value', value: '数值' },
  { key: 'buttons', value: '按钮组' },
  { key: 'sql', value: '查询语句 (SQL字段必填)' },
]

const EntityFieldDataType = [
  { key: 'string', value: '字符串' },
  { key: 'number', value: '数字' },
  { key: 'rich_text', value: '富文本' },
  { key: 'date', value: '日期' },
  { key: 'price', value: '价格' },
  { key: 'dict', value: '字典 (dict_list)' },
  { key: 'datetime', value: '日期时间' },
  { key: 'time', value: '时间' },
  { key: 'list', value: '列表' },
  { key: 'key_value', value: '键值对' },
  { key: 'switch', value: '开关' },
  { key: 'boolean', value: '布尔类型' },
  { key: 'global-component', value: '全局组件 (form_component)' },
  { key: 'foreign-key', value: '外键' },
  { key: 'text-area', value: '多行文本' },
]

const EntityForeignType = [
  { key: 'one-to-one', value: '一对一' },
  { key: 'many-to-many', value: '多对多' },
  // { key: 'one-to-many', value: '一对多' },
  // { key: 'many-to-one', value: '多对一' },
]

const EntityFieldDisplayType = [
  { key: 'auto', value: '默认' },
  { key: 'iframe', value: 'Iframe (iframe_url)' },
  { key: 'global-component', value: '全局组件 (display_component)' },
]

const EntityDataType = [{
  key: 'db_table',
  value: '数据表（数据表名 字段）',
}, {
  key: 'analysis',
  value: '数据统计',
}, {
  key: 'sql',
  value: '查询语句（SQL 字段）',
}]

const PageSectionType = [{
    key: 'page',
    value: '页面',
  }, {
    key: 'tab',
    value: 'Tab',
  }, {
    key: 'details',
    value: '详情',
  }, {
    key: 'form',
    value: '表单',
  }, {
    key: 'search',
    value: '搜索',
  }, {
    key: 'html',
    value: 'HTML脚本',
  }, {
    key: 'buttons',
    value: '按钮组',
  }, {
    key: 'list',
    value: '列表',
  }, {
    key: 'analysis',
    value: '数据统计',
  }]

export default {
  MenuType,
  DefaultMenu,
  PageDirection,
  DefaultPage,
  DefaultPageSection,
  DefaultEntity,
  DefaultEntityField,
  ButtonType,
  EntityFieldExists,
  EntityFieldType,
  EntityFieldDataType,
  EntityFieldDisplayType,
  EntityDataType,
  PageSectionType,

  EntityForeignType,
  EntityFieldLinkType,
}
