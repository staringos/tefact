<template>
  <div class="editor-wrapper" v-if="engine.target" @click="handleEditorClick">
    <div class="editor-container">
      <Toolbar :target="currentTarget || form"></Toolbar>
      <div class="editor-main">
        <NodesBar :editorType="editorType" />
        <div class="editor-container">
          <img
            v-if="isMobile"
            class="phone-bg"
            :src="require('../assets/images/GooglePhone.png')"
          />
          <div v-if="!isMobile" class="page-pad">
            <Page
              v-if="!engine.isForm"
              :page="currentTarget"
              :pageId="pageId"
              :isMobile="isMobile"
            />
            <Form
              v-else
              :form="currentTarget"
              :isEdit="true"
              :isMobile="isMobile"
            />
          </div>
          <div v-else class="page-pad mobile">
            <div class="inner">
              <Page
                v-if="!isForm"
                :page="currentTarget"
                :pageId="pageId"
                :isMobile="isMobile"
              />
              <Form
                v-else
                :form="currentTarget"
                :isEdit="true"
                :isMobile="isMobile"
              />
            </div>
          </div>
        </div>
      </div>
    </div>
    <PropertiesBar />
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
import { Component, Prop, Watch } from "vue-property-decorator";
import Page from "@tefact/feature-page";
import Form from "@tefact/feature-form";
import Toolbar from "TEFACT_EDITOR/components/Toolbar.vue";
import PropertiesBar from "@tefact/properties";
import NodesBar from "TEFACT_EDITOR/components/NodesBar.vue";
import Engine, { BaseView, ISetting, ITarget, EVENT } from "@tefact/core";

@Component({
  components: { NodesBar, Toolbar, PropertiesBar, Page, Form },
  // mixins: [BaseView]
})
export default class Editor extends BaseView {
  @Prop() value?: ITarget;
  @Prop() editorSetting?: ISetting;

  pageId: string | null = null;

  get isMobile(): boolean {
    return this.setting?.device === "mobile";
  }

  get currentTarget() {
    return this.engine.target;
  }

  get editorType(): string {
    if (this.isForm) return "form";
    if (this.setting?.device) return this.setting?.device;
    return "pc";
  }

  @Watch("value", { immediate: true })
  handleTargetChange(): void {
    this.init();
  }

  init(): void {
    // eslint-disable-next-line @typescript-eslint/no-this-alias
    const that = this;
    if (that.engine.target === this.value) return;

    function execEvent(type: string, noInput = false) {
      return (data: ITarget) => {
        !noInput && that.$emit(EVENT.INPUT, data);
        that.$emit(type, data);
      };
    }

    this.engine = Engine.instance(this.value, this.editorSetting);
    this.engine.on(EVENT.ADD, execEvent(EVENT.ADD));
    this.engine.on(EVENT.UPDATE, execEvent(EVENT.UPDATE));
    this.engine.on(EVENT.UPDATE_CONFIG, execEvent(EVENT.UPDATE_CONFIG));
    this.engine.on(EVENT.SAVE, execEvent(EVENT.SAVE));
    this.engine.on(EVENT.SHARE, execEvent(EVENT.SHARE));
    this.engine.on(EVENT.OPEN_MODIFIER, execEvent(EVENT.OPEN_MODIFIER, true));
    this.engine.on(EVENT.BACK, execEvent(EVENT.BACK, true));
  }

  handleEditorClick() {
    this.engine.activeNode(["null"]);
  }

  handleEditorSettingChange(es: ISetting): void {
    console.log("es:", es);
    //   this.setting = es;
  }
}
</script>
