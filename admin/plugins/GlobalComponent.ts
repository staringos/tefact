import { Vue } from 'nuxt-property-decorator'
// import arrplat from '../.arrplat.json'

function interopDefault(promise) {
  return promise.then(m => m.default || m)
}

const GlobalComponents = {
  'EntityModifier': () => interopDefault(import('../components/entities/EntityModifier.vue'))
}

export default async function() {
  if (process.server) return

  // const plus = arrplat.plus.plus
  // plus.map(plus => {
  //   const components = plus.globalComponents as any[]
  //   if (!components) return
  //   components.map(async (that) => {
  //     Vue.component(that.name, await GlobalComponents[that.name])
  //   })
  // })
}
