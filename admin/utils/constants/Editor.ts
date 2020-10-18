import { ImageNodeModel, TextNodeModel, TableNodeModel, ButtonNodeModel } from '~/utils/entities/editor/node';
import { cloneDeep } from "lodash"

export const BorderStyle = [
  { value: 'solid', label: '直线' },
  { value: 'dotted', label: '短虚线' },
  { value: 'dashed', label: '长虚线' },
  { value: 'double', label: '双层' },
]

export const NodeResoluConfig = {
  text: {
    title: '文字元素配置',
    hasTab: true,
    tabs: [
      {
        title: '基本信息',
        components: [
          { type: 'PositionResolu', params: {} },
          { type: 'BackgroundResolu', params: {} },
          { type: 'BorderResolu', params: {} },
          { type: 'TextResolu', params: {} },
        ],
      }, {
        title: '数据展示',
        components: [],
      },
    ],
  },
  image: {
    title: '图片配置',
    hasTab: true,
    tabs: [
      {
        title: '基本信息',
        components: [
          { type: 'PositionResolu', params: {} },
          { type: 'BackgroundResolu', params: {} },
          { type: 'BorderResolu', params: {} },
          { type: 'TextResolu', params: {} },
        ],
      }, {
        title: '数据展示',
        components: [],
      },
    ],
  },
  page: {
    title: '页面配置',
    hasTab: true,
    tabs: [
      {
        title: '基本信息',
        components: [
          { type: 'BackgroundResolu', params: {} },
          { type: 'BorderResolu', params: {} },
        ],
      },
    ],
  },
  section: {
    title: '段落配置',
    hasTab: true,
    tabs: [
      {
        title: '基本信息',
        components: [
          { type: 'BackgroundResolu', params: {} },
          { type: 'BorderResolu', params: {} },
        ],
      },
    ],
  },
  table: {
    title: '数据表配置',
    hasTab: true,
    tabs: [
      {
        title: '基本信息',
        components: [
          { type: 'BackgroundResolu', params: {} },
          { type: 'BorderResolu', params: {} },
        ],
      },
      {
        title: '数据',
        components: [
          { type: 'EntityResolu', params: {} },
        ],
      },
    ],
  },
  button: {
    title: '按钮配置',
    hasTab: true,
    tabs: [
      {
        title: '基本信息',
        components: [
          { type: 'BackgroundResolu', params: {} },
          { type: 'BorderResolu', params: {} },
          {
            type: 'RowsResolu', params: {
              title: '按钮设置',
              rows: [{
                type: 'SelectRow',
                params: {
                  title: "类型",
                  path: "data.type",
                  selectOptions: [
                    {value: 'primary', label: 'Primary'},
                    {value: 'info', label: 'Info'},
                    {value: 'warning', label: 'Warning'},
                    {value: 'danger', label: 'Danger'},
                    {value: 'text', label: 'Text'},
                    {value: 'success', label: 'Success'},
                  ]
                }
              }, {
                type: 'SwitchRow',
                params: {
                  title: "朴素按钮",
                  path: "data.plain"
                }
              }, {
                type: 'SwitchRow',
                params: {
                  title: "圆角",
                  path: "data.round"
                }
              }, {
                type: 'SwitchRow',
                params: {
                  title: "圆形",
                  path: "data.circle"
                }
              }]
            }
          }
        ],
      },
      {
        title: '数据',
        components: [
          { type: 'EntityResolu', params: {} },
        ],
      },
    ],
  },
}

export const NodeTypeToComponent = {
  text: "TextNode",
  image: "ImageNode",
  html: "HtmlNode",
  table: "TableNode",
  button: "ButtonNode",
}

export const BaseNodeStyle = {
  'border-width': 0,
  'font-size': 12,
  'font-color': '#333',
}

export const BaseNodeConfig = {
  x: 30,
  y: 30,
  w: 120,
  h: 80,
  style: { ...BaseNodeStyle },
}

export const getBaseNodeConfig = () => cloneDeep(BaseNodeConfig);

export const NodeDefaultData = {
  page: {
    config: {
      style: { ...BaseNodeStyle },
    },
  },
  section: {
    config: {
      style: { ...BaseNodeStyle },
    },
  },
  text: {
    type: 'text',
    config: getBaseNodeConfig(),
    data: {
      text: '请输入文字',
    },
  } as TextNodeModel,
  button: {
    type: 'button',
    config: { ...getBaseNodeConfig(), w: 98, h: 40 },
    data: {
      text: '按钮',
      type: 'primary'
    },
  } as ButtonNodeModel,
  image: {
    type: 'image',
    config: getBaseNodeConfig(),
    data: {
      url: null,
      title: '',
    },
  } as ImageNodeModel,
  table: {
    type: 'table',
    config: getBaseNodeConfig(),
    data: {
      dataSourceId: null,
      entityId: null,
      url: null,
      title: '',
    },
  } as TableNodeModel,
}

export const NodeListConstants = [
  {
  icon: 'tf-icon-Text',
  type: 'text',
  title: '文字',
  nodeData: NodeDefaultData.text,
}, {
  icon: 'tf-icon-image',
  type: 'image',
  title: '图片',
  nodeData: NodeDefaultData.image,
}, {
  icon: 'tf-icon-iconfonticonbiaoge',
  type: 'table',
  title: '数据表',
  nodeData: NodeDefaultData.table,
}, {
  icon: 'tf-icon-code',
  type: 'html',
  title: 'HTML',
}, {
  icon: 'tf-icon-integral',
  type: 'div',
  title: '层',
}, {
  icon: 'tf-icon-nav-list',
  type: 'list',
  title: '列表',
}, {
  icon: 'tf-icon-mtbutton',
  type: 'button',
  title: '按钮',
  nodeData: NodeDefaultData.button
}]
