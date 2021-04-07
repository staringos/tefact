import { Component } from 'vue-property-decorator'
import { BaseView } from '@tefact/core'
import type { IBaseNode } from '@tefact/core'

@Component
export default class PropertiesClass extends BaseView {
  tmpNode!:IBaseNode;

  handleSave() {}
}
