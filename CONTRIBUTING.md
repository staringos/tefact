# Contributing Guides

First off, thank you for considering contributing to Tefact. It's people like you that make Tefact such a great tool.

[source: [Active Admin](https://github.com/Tefact/tefact-saas/blob/master/CONTRIBUTING.md)] 

**Need more inspiration?** 

[1] [Read The README](http://read-the-docs.readthedocs.org/en/latest/contribute.html) 

[2] [VUE.js](https://github.com/vuejs/vue)

[3] [ElementUI](https://github.com/ElemeFE/element)

## Admin Panel

### File Template

Vue Components 

```vue
<template>
  <div>

  </div>
</template>
<style lang="scss" scoped>

</style>
<script lang="ts">
  import { Vue, Component } from 'nuxt-property-decorator'

  @Component
  export default class AppItem extends Vue {

  }
</script>
```

## Mobile

File Template

#### Mobile Container components

```react
import { ComponentClass } from 'react'
import Taro from '@tarojs/taro'
import { connect } from '@tarojs/redux'
import { View } from '@tarojs/components'

import AppPageLayout from '../../../layout/AppPageLayout'

type PageStateProps = {}
type PageDispatchProps = {}
type PageOwnProps = {}
type PageState = {}
type IProps = PageStateProps & PageDispatchProps & PageOwnProps

interface Index {
  props: IProps
  state: PageState
}

@connect(() => ({
  }),
  (dispatch) => ({
  }),
)
class Index extends Taro.PureComponent {
  public render() {
    return (<AppPageLayout>
      <View />
    </AppPageLayout>)
  }
}

export default Index as ComponentClass<PageOwnProps, PageState>
```
