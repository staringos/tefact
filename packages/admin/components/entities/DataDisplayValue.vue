<template>
  <span v-if="field.data_type === 'date'" class="text">{{transformTime(data[field.key], 'date')}}</span>
  <span v-else-if="field.data_type === 'global-component'" class="text">
    <component :is="field.display_component" :field="field" :row="data"></component>
  </span>
  <span v-else-if="field.data_type === 'dict'">{{findDict(field, data)}}</span>
  <span v-else-if="field.data_type === 'datetime'" class="text">{{transformTime(data[field.key], 'datetime')}}</span>
  <span v-else-if="field.data_type === 'time'">{{transformTime(data[field.key], 'time')}}</span>
  <span v-else-if="field.data_type === 'boolean'">{{data[field.key] === 1 ? '是' : '否'}}</span>
  <span v-else-if="field.data_type === 'list'">
    <p v-for="(row, i) in data[field.key]" :key="i">{{row.value}}</p>
  </span>
  <span v-else-if="field.data_type === 'key_value'">{{data[field.key] && data[field.key].value}}</span>
  <span v-else-if="field.data_type === 'foreign-key' && field.foreign_type === 'one-to-one'">{{data[field.key] && data[field.key]}}</span>
  <span v-else>{{data[field.key]}}</span>
</template>
<script lang="ts">
  import { Component, Vue, Prop } from 'nuxt-property-decorator'
  import List from './List.vue'
  import EntityModifier from './EntityModifier.vue'
  import EntityButton from './EntityButton.vue'
  import { transformTime } from '~/utils'

  @Component({
      components: { List, EntityModifier, EntityButton }
  })
  export default class DataDisplay extends Vue {
    @Prop() field
    @Prop() data

    transformTime = transformTime

    public findDict(field, row) {
      if (!field.dict_list) return row[field.key]
      const dict = field.dict_list.filter(dict => dict.key == row[field.key])
      if (dict && dict.length > 0) return dict[0].value
      return row[field.key]
    }
  }
</script>
