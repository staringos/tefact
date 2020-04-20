import { Vue } from 'nuxt-property-decorator'
import { Builder } from '@arrplat/core'
import appConfig from '../../../arrplat.config.json'

function interopDefault(promise) {
  return promise.then(m => m.default || m)
}

const GlobalComponents = {
  'arrplat-education-color': () => interopDefault(import('@arrplat/education/admin/components/global/Color.vue')),
  'arrplat-education-colormodify': () => interopDefault(import('@arrplat/education/admin/components/global/ColorModify.vue')),
  'EntityModifier': () => interopDefault(import('../components/entities/EntityModifier.vue'))
}

export default async function() {
  if (process.server) return
  const options = await Builder.build(appConfig)
  const plus = options.plus.plus
  plus.map(plus => {
    const components = plus.globalComponents as any[]
    if (!components) return
    components.map(async (that) => {
      Vue.component(that.name, await GlobalComponents[that.name])
    })
  })
}
