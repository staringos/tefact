<template>
  <div class="editor-wrapper" v-if="currentPage || form" @click="resetActive">
    <div class="editor-container">
      <Toolbar
        :item="currentPage || form"
        :isForm="isForm"
        :editorSetting="editorSetting"
        :editorType="editorType"
        @editorSettingChange="handleEditorSettingChange"
      ></Toolbar>
      <div class="editor-main">
        <NodesBar :editorType="editorType" />
        <div class="editor-container">
          <img v-if="isMobile" class="phone-bg" src="/images/GooglePhone.png" />

          <div v-if="!isMobile" class="page-pad">
            <Page
              v-if="!isForm"
              :page="currentPage"
              :pageId="pageId"
              :isMobile="isMobile"
            />
            <Form v-else :form="form" :isEdit="true" :isMobile="isMobile" />
          </div>
          <div v-else class="page-pad mobile">
            <div class="inner">
              <Page
                v-if="!isForm"
                :page="currentPage"
                :pageId="pageId"
                :isMobile="isMobile"
              />
              <Form v-else :form="form" :isEdit="true" :isMobile="isMobile" />
            </div>
          </div>
        </div>
      </div>
    </div>
    <Sidebar />
  </div>
</template>
<style lang="scss" scoped>
.editor-wrapper {
  display: flex;
  flex: 1;
  overflow: hidden;

  .editor-container {
    background: #f0f2f5;
    flex: 3;
    display: flex;
    flex-direction: column;

    .editor {
      flex: 1;
      overflow: auto;
    }

    .editor-main {
      -webkit-box-flex: 1;
      flex-grow: 1;
      display: flex;
      overflow: auto;
      flex-direction: row;
      padding: 0;

      .editor-container {
        flex-grow: 1;
        overflow: auto;
        flex-direction: row;
        padding: 20px 20px 0 20px;
        width: 0;
        position: relative;

        .phone-bg {
          width: 425px;
          height: 765px;
          position: absolute;
          top: 5px;
          left: calc(50% - 212.5px);
          z-index: 1;
        }

        .page-pad {
          .inner {
            width: 100%;
            height: 100%;
            flex: 1;
            overflow: auto;
          }

          &:not(.mobile) {
            padding-right: 20px;
            // flex: 1;
          }

          &.mobile {
            display: flex;
            width: 375px;
            height: 667px;
            overflow: hidden;
            position: absolute;
            top: 60px;
            z-index: 20;
            background: $editorBackground;
            left: calc(50% - 187.5px);

            ::v-deep.editor-page-canvas.column-side {
              overflow: hidden;
            }
          }
        }
      }
    }
  }
}
</style>
<script lang="ts">
import { Vue, Component, Prop } from "vue-property-decorator";
import Page from "@tefact/feature-page";
import Form, { IForm } from "@tefact/feature-form";
import Toolbar from "@/components/Toolbar.vue";
import PropertiesBar from "@/components/PropertiesBar.vue";
import NodesBar from "@/components/NodesBar.vue";

@Component({
  components: { NodesBar, Toolbar, PropertiesBar, Page, Form }
})
export default class Editor extends Vue {
  currentPage = {
    title: "这是一个新页面"
  };

  @Prop() form?: IForm;
  @Prop(Boolean) isForm?: boolean;

  pageId: string | null = null;

  editorSetting = {
    device: "pc"
  };

  get isMobile(): boolean {
    return this.editorSetting.device === "mobile";
  }

  get editorType(): string {
    if (this.isForm) {
      // if (this.isForm || this.currentNode && this.currentNode.type === 'FormNode') {
      return "form";
    }

    if (this.editorSetting.device) {
      return this.editorSetting.device;
    }

    return "pc";
  }

  async init() {
    console.log("init");
  }

  handleEditorSettingChange(es: any) {
    this.editorSetting = es;
  }
}
</script>
