<template>
  <div class="form-item" @hover.stop @mouseover.stop>
    <el-form-item :label="item.label" :prop="item.key">
      <component :item="item" :is="item.type" />
    </el-form-item>
  </div>
</template>
<style lang="scss" scoped>
  .form-item {
    flex: 1;
    width: 100%;
    box-sizing: border-box;
    padding: 10px;

    &:hover {
      border: 1px solid $editor-border-active-color;
    }

    ::v-deep .el-form-item {
      display: flex;
    }
  ;
  }
</style>
<script lang="ts">
import { Vue, Component, Prop } from 'nuxt-property-decorator'
import { FormItemModel } from "~/utils/entities/editor/form"
import InputNode from './fields/InputNode.vue'

@Component({
  components: {
    InputNode
  }
})
export default class FormItem extends Vue {
  @Prop() item!: FormItemModel
}
</script>
