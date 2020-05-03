import { TextNodeModel } from '~/utils/entities/editor/node'

export const NodeTypeToComponent = {
  text: "TextNode",
  image: "ImageNode",
  html: "HtmlNode",
}

export const NodeListConstants = [{
  icon: 'tf-icon-Text',
  type: 'text',
  title: '文字',
  nodeData: {
    type: 'text',
    config: {
      x: 30,
      y: 30,
      w: 100,
      h: 80,
      style: []
    },
    data: {
      text: '请输入文字'
    }
  } as TextNodeModel
}, {
  icon: 'tf-icon-image',
  type: 'image',
  title: '图片'
}, {
  icon: 'tf-icon-code',
  type: 'html',
  title: 'HTML'
}, {
  icon: 'tf-icon-integral',
  type: 'div',
  title: '层'
}, {
  icon: 'tf-icon-nav-list',
  type: 'list',
  title: '列表'
}, {
  icon: 'tf-icon-mtbutton',
  type: 'button',
  title: '按钮'
}]
