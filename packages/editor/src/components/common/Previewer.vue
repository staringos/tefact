<template>
  <el-dialog
    title="页面预览"
    :visible.sync="show"
    class="page-previewer"
    :before-close="() => $emit('cancel')"
    fullscreen
  >
    <div class="page-container" v-if="page">
      <div class="header"></div>
      <div class="content">
        <Page v-if="!isForm" :page="page" :pageId="page.id" :preview="true" />
        <Form v-else :form="page" :preview="true" />
      </div>
    </div>
  </el-dialog>
</template>
<style lang="scss" scoped>
.page-previewer {
  height: 100vh;
  overflow: hidden;
  display: flex;

  ::v-deep .el-dialog {
    display: flex;
    flex-direction: column;

    .el-dialog__body {
      flex: 1;
      padding-top: 0;
      overflow: hidden;
      display: flex;
    }
  }
}

.page-container {
  overflow: hidden;
  box-shadow: 0 6px 20px 5px rgba(40, 120, 255, 0.1),
    0 16px 24px 2px rgba(0, 0, 0, 0.05);
  display: flex;
  flex: 1;
  flex-direction: column;

  .header {
    width: 100%;
    height: 45px;
    background: url(/images/browser.png) left top/100% no-repeat;
  }

  .content {
    overflow: auto;
    flex: 1;
  }
}
</style>
<script lang="ts">
import { Vue, Component, Prop } from "vue-property-decorator";
import Page from "@tefact/feature-page";
import Form from "@tefact/feature-form";
import { ITarget } from "@tefact/core";

@Component({
  components: { Page, Form }
})
export default class Previewer extends Vue {
  @Prop() page!: ITarget;
  @Prop(Boolean) isForm!: boolean;
  @Prop(Boolean) show!: boolean;
}
</script>
