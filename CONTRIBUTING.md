# Contribute to Tefact


## Admin Panel

### File Template

Vue Components 

```vue
<template>
  <div>

  </div>
</template>
<style lang="scss">

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
