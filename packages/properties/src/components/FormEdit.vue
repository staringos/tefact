<template>
  <div class="modify-form" v-if="editData">
    <component
      v-for="(row, i) in rows"
      :key="i"
      :index="i"
      :is="row.type"
      :nodeType="nodeType"
      :node="tmpData"
      v-bind="row.params"
      :isDirectModify="true"
      @modify="handleModify"
      :row="row"
    ></component>
    <el-button size="small" type="primary" @click="$emit('confirm', tmpData)"
      >确定</el-button
    >
    <el-button size="small" type="default" @click="$emit('cancel')"
      >取消</el-button
    >
  </div>
</template>
<script>
import { Vue, Component, Prop, Watch } from "vue-property-decorator";
import Rows from "../rows";

@Component({
  components: { ...Rows },
})
export default class FormEdit extends Vue {
  @Prop([Array]) rows;
  @Prop([String]) nodeType;
  @Prop([Object, null]) editData;

  tmpData = null;

  handleModify(data) {
    this.tmpData = data;
  }

  @Watch("editData", { immediate: true })
  handleDataChange() {
    this.tmpData = this.editData;
  }
}
</script>
