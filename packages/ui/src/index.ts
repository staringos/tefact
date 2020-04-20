import DialogX from './components/DialogX.vue'
import ArrPanel from './components/ArrPanel.vue'
import ArrTitle from './components/ArrTitle.vue'
import List from './components/List.vue'
import AvatarUploader from './components/AvatarUploader.vue'
import AttributeList from './components/AttributeList.vue'
import Confirm from './components/Confirm'

const components = [
  DialogX,
  ArrPanel,
  List,
  ArrTitle,
  AttributeList,
  AvatarUploader
]

const install = function(Vue, opts = {}) {
  components.forEach(component =>
    Vue.component((component as any).name, component))
}

/* istanbul ignore if */
// if (typeof window !== 'undefined' && window.Vue) {
//   install(window.Vue);
// }

export default {
  install,
  DialogX,
  ArrPanel,
  List,
  AvatarUploader,
  AttributeList,
  ArrTitle,
  Confirm
}
