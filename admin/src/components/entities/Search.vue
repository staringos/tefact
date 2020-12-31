<template>
  <div class="search-container">
    <el-form :inline="true" class="search-main">
      <FieldFormItem :form="form" :entity="section.entity" @change="handleFormChange" where="search" />

      <el-form-item style="float: left;">
        <el-button type="default" @click="handleSubmit" round size="small">搜 索</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>
<style lang="scss">
  .search-container {
    background-color: #f5f5f5;
    border-radius: 5px;
    padding: 20px 20px 0 20px;
    margin-bottom: 10px;

    .search-main  {
      display: flex;
    }
  }
</style>
<script lang="ts">
  import { Component, Vue, Prop, namespace } from 'nuxt-property-decorator'
  import { EntityPageSection } from '~/services/common/entities/entities'
  import FieldFormItem from './FieldFormItem.vue'
  import { deepCopy } from '~/utils'

  @Component({
    components: {
      FieldFormItem
    }
  })
  export default class Search extends Vue {
    @Prop(Object) section!: EntityPageSection
    @Prop({ default: {}, type: Object }) value!: EntityPageSection
    @Prop(Function) onSearch

    form = {}

    handleSubmit() {
      const conditions = [] as any[]

      for (let key in this.form) {
        const value = this.form[key]
        conditions.push({
          field_name: key,
          value,
          search_type: typeof value === 'string' ? 1:0
        })
      }

      this.onSearch(conditions)
    }

    handleFormChange (form) {
      this.form = { ...form }
    }

    mounted() {
      this.form = deepCopy(this.value)
    }
  }
</script>
