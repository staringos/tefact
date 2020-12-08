import { ImageNodeModel, TextNodeModel, TableNodeModel, ButtonNodeModel } from '~/utils/entities/editor/node';
import cloneDeep from 'lodash/cloneDeep'
import isNumber from 'lodash/isNumber'

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
  BrowserNode: {
    title: '网页配置',
    hasTab: true,
    tabs: [
      {
        title: '基本信息',
        components: [
          {type: 'PositionResolu', params: {}},
          {type: 'BackgroundResolu', params: {}},
          {type: 'BorderResolu', params: {}},
          {type: 'TextResolu', params: {}},
        ],
      }, {
        title: '数据展示',
        components: [
          {
            type: 'RowsResolu', params: {
              title: '网页内容设置',
              rows: [{
                type: 'TextRow',
                params: {
                  title: '链接',
                  path: "data.src"
                }
              }]
            }
          }
        ],
      },
    ],
  },
  FormNode: {
    title: '表单配置',
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
        components: [
          {
            type: 'RowsResolu', params: {
              title: '卡片内容设置',
              rows: [{
                type: 'TextRow',
                params: {
                  title: "标题",
                  path: "data.title"
                }
              }, {
                type: 'TextareaRow',
                params: {
                  title: "内容",
                  path: "data.content"
                }
              }]
            }
          }
        ],
      },
    ],
  },
  CardNode: {
    title: '卡片配置',
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
        components: [
          {
            type: 'RowsResolu', params: {
              title: '卡片内容设置',
              rows: [{
                type: 'TextRow',
                params: {
                  title: "标题",
                  path: "data.title"
                }
              }, {
                type: 'TextareaRow',
                params: {
                  title: "内容",
                  path: "data.content"
                }
              }]
            }
          }
        ],
      },
    ],
  },
  CarouselNode: {
    title: '轮播图配置',
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
        components: [
          {
            type: 'ListResolu',
            params: {
              title: '轮播图内容设置',
              path: 'data.list',
              rows: [{
                type: 'TextRow',
                params: {
                  title: "标题",
                  path: "title"
                }
              }, {
                type: 'TextRow',
                params: {
                  title: "描述",
                  path: "desc"
                }
              }, {
                type: 'TextRow',
                params: {
                  title: "图片",
                  path: "image"
                }
              }, {
                type: 'TextRow',
                params: {
                  title: "超链接",
                  path: "link"
                }
              }]
            }
          }
        ],
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
          {
            type: 'RowsResolu', params: {
              title: '布局设置',
              rows: [{
                type: 'SelectRow',
                params: {
                  title: "布局模式",
                  path: "config.viewMode",
                  selectOptions: [
                    {value: 'fixed', label: '固定'},
                    {value: 'adapt', label: '适配'},
                  ]
                }
              }, {
                type: 'NumberRow',
                params: {
                  title: "页面宽度",
                  unit: "px",
                  path: "config.style.width"
                }
              }]
            }
          }
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
  button: "ButtonNode"
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

export const getBaseNodeConfig = (width?: number, height?: number) => {
  const res = cloneDeep(BaseNodeConfig);
  if (isNumber(width)) {
    res.w = width
  }

  if (isNumber(height)) {
    res.h = height
  }
  return res;
}

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
  CardNode: {
    type: 'CardNode',
    config: getBaseNodeConfig(),
    data: {
      title: "卡片标题",
      content: "卡片内容"
    },
  },
  BrowserNode: {
    type: 'BrowserNode',
    config: getBaseNodeConfig(),
    data: {
      src: 'https://tefact.com'
    }
  },
  CarouselNode: {
    type: 'CarouselNode',
    config: getBaseNodeConfig(),
    data: {
      list: [{
        image: '/images/image.png',
        title: 'Default Image',
        desc: 'Default Image',
        link: 'http://saas.tefact.com'
      }, {
        image: '/images/image.png',
        title: 'Default Image',
        desc: 'Default Image',
        link: 'http://saas.tefact.com'
      }, {
        image: '/images/image.png',
        title: 'Default Image',
        desc: 'Default Image',
        link: 'http://saas.tefact.com'
      }],
    },
  },
  FormNode: {
    type: 'FormNode',
    config: getBaseNodeConfig(350, 390),
    data: {
      formId: null
    },
  }
}

export const FormNodeList = [
  {
    icon: 'tf-icon-input',
    type: 'InputNode',
    title: '文字',
    nodeData: NodeDefaultData.text,
  }, {
    icon: 'tf-icon-date',
    type: 'DateNode',
    title: '日期',
    nodeData: NodeDefaultData.text,
  }, {
    icon: 'tf-icon-money',
    type: 'MoneyNode',
    title: '价格',
    nodeData: NodeDefaultData.text,
  }, {
    icon: 'tf-icon-number',
    type: 'NumberNode',
    title: '数字',
    nodeData: NodeDefaultData.text,
  }, {
    icon: 'tf-icon-phone',
    type: 'PhoneNode',
    title: '手机号',
    nodeData: NodeDefaultData.text,
  }, {
    icon: 'tf-icon-radio',
    type: 'RadioNode',
    title: '单选框',
    nodeData: NodeDefaultData.text,
  }, {
    icon: 'tf-icon-select',
    type: 'SelectNode',
    title: '下拉框',
    nodeData: NodeDefaultData.text,
  }, {
    icon: 'tf-icon-slider',
    type: 'SliderNode',
    title: '数字区间',
    nodeData: NodeDefaultData.text,
  }, {
    icon: 'tf-icon-qq',
    type: 'QQNode',
    title: 'QQ号',
    nodeData: NodeDefaultData.text,
  }, {
    icon: 'tf-icon-switch',
    type: 'SwitchNode',
    title: '开关',
    nodeData: NodeDefaultData.text,
  }, {
    icon: 'tf-icon-textarea',
    type: 'TextAreaNode',
    title: '多行文本',
    nodeData: NodeDefaultData.text,
  }, {
    icon: 'tf-icon-time',
    type: 'TimeNode',
    title: '时间',
    nodeData: NodeDefaultData.text,
  }, {
    icon: 'tf-icon-upload',
    type: 'FileNode',
    title: '文件',
    nodeData: NodeDefaultData.text,
  }, {
    icon: 'tf-icon-checkbox',
    type: 'CheckboxNode',
    title: '多选框',
    nodeData: NodeDefaultData.text,
  }, {
    icon: 'tf-icon-date-range',
    type: 'TextAreaNode',
    title: '时间区间',
    nodeData: NodeDefaultData.text,
  }, {
    icon: 'tf-icon-editor',
    type: 'EditorNode',
    title: '富文本',
    nodeData: NodeDefaultData.text,
  }
]

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
}, {
  icon: 'tf-icon-browser',
  type: 'BrowserNode',
  title: '网页',
  nodeData: NodeDefaultData.BrowserNode
  }, {
  icon: 'tf-icon-lunbotu',
  type: 'CarouselNode',
  title: '轮播图',
  nodeData: NodeDefaultData.CarouselNode
}, {
  icon: 'tf-icon-navs',
  type: 'NavNode',
  title: '导航',
}, {
  icon: 'tf-icon-card',
  type: 'CardNode',
  title: '卡片',
  nodeData: NodeDefaultData.CardNode
}, {
  icon: 'tf-icon-form',
  type: 'FormNode',
  title: '表单',
  nodeData: NodeDefaultData.FormNode
},
]
