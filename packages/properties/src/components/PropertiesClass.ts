import { Component } from 'vue-property-decorator'
import { BaseView, IBaseNode } from '@tefact/core'

@Component
export default class PropertiesClass extends BaseView {
  tmpNode!:IBaseNode;

  handleSave() {}
}
