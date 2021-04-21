<template>
  <el-dialog
      title="数据项管理"
      :visible.sync="value"
      class="page-previewer"
      :before-close="() => $emit('cancel')"
      width="500px"
  >
    <div class="dataset-wrapper">
      <div></div>
      <div></div>
    </div>
  </el-dialog>
</template>
<script lang="ts">
import { Component, Prop } from "vue-property-decorator"
import Previewer from "../common/Previewer.vue";
import SharePageEditor from "../common/SharePageEditor.vue";
import {BaseView} from "../../../../core";

@Component({
  components: { Previewer, SharePageEditor },
})
export default class DataSetDialog extends BaseView {
  @Prop(Boolean) value
}
</script>