import { TextNodeModel } from '~/utils/entities/editor/node'

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
  page: {
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
  section: {
    title: '页面配置',
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
}

export const NodeTypeToComponent = {
  text: "TextNode",
  image: "ImageNode",
  html: "HtmlNode",
}

export const NodeDefaultData = {
  page: {
    config: {
      style: {},
    },
  },
  section: {
    config: {
      style: {},
    },
  },
  text: {
    type: 'text',
    config: {
      x: 30,
      y: 30,
      w: 100,
      h: 80,
      style: {},
    },
    data: {
      text: '请输入文字',
    },
  } as TextNodeModel,
}

export const NodeListConstants = [{
  icon: 'tf-icon-Text',
  type: 'text',
  title: '文字',
  nodeData: NodeDefaultData.text,
}, {
  icon: 'tf-icon-image',
  type: 'image',
  title: '图片',
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
}]
