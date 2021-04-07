<template>
  <div
    :class="`page-content ${this.isMobileInDesktop ? 'desktop-mobile' : ''}`"
  >
    <Page
      v-if="!isMobileInDesktop && page.feature_type === 'page' && page"
      :page="page"
      :pageId="page.id"
      :preview="true"
      :editorSetting="setting"
    />
    <Form
      v-if="!isMobileInDesktop && page.feature_type === 'form' && page"
      :form="page"
      :pageId="page.id"
      :preview="true"
      @submit="$emit('submit', $event)"
    />
    <div v-if="isMobileInDesktop" class="mobile-in-desktop">
      <div class="left-block">
        <img v-if="isMobile" class="phone-bg" src="/images/GooglePhone.png" />

        <div class="inner">
          <Page
            v-if="page.feature_type === 'page' && page"
            :page="page"
            :pageId="page.id"
            :preview="true"
            :editorSetting="setting"
          />
          <Form
            v-if="page.feature_type === 'form' && page"
            :form="page"
            :pageId="page.id"
            :preview="true"
            @submit="$emit('submit', $event)"
          />
        </div>
      </div>
      <div class="info-block">
        <h2>{{ page.title }}</h2>
        <p>{{ page.direction }}</p>
        <div class="link-input-panel">
          <el-input class="link-input" :value="link" :disabled="true" />
          <el-button size="small" @click="handleCopy">点击复制</el-button>
        </div>
        <div v-if="this.qrcode">
          <img :src="qrcode" />
          <p class="sub-description">手机扫码获取页面</p>
        </div>
        <div class="musk" v-if="!page.share">
          <p class="text">请分享后查看...</p>
        </div>
      </div>
    </div>
    <div class="power-by">
      Power by <a href="https://staringos.com" target="_blank">StaringOS</a>
    </div>
  </div>
</template>
<style lang="scss" scoped>
.page-content {
  width: 100%;
  height: auto;
  min-height: 100%;
  display: flex;
  flex-direction: column;
  padding-bottom: 20px;

  &.desktop-mobile {
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .mobile-in-desktop {
    width: 80%;
    height: 805px;
    display: flex;
    background-color: white;
    border-radius: 20px;
    padding: 20px;

    .left-block {
      display: flex;
      width: 425px;
      position: relative;

      .phone-bg {
        width: 425px;
        height: 765px;
        position: absolute;
        left: 0;
        top: 0;
        z-index: 1;
      }

      .inner {
        width: 375px;
        height: 667px;
        overflow: auto;
        position: absolute;
        top: 60px;
        z-index: 20;
        left: calc(50% - 187.5px);
        background-color: #f5f5f5;
      }

      ::v-deep.editor-page-canvas.column-side {
        overflow: hidden !important;
      }
    }

    .info-block {
      flex: 1;
      margin-left: 50px;
      padding-top: 50px;
      position: relative;

      .link-input-panel {
        display: flex;
        margin-top: 20px;
        margin-bottom: 20px;

        .link-input {
          margin-right: 20px;
          //::v-deep .el-input__inner {
          //  text-shadow: 0 0 8px rgb(109 109 109);
          //}
        }
      }

      .musk {
        position: absolute;
        top: 95px;
        left: 0;
        box-shadow: 0 0 8px rgb(109 109 109);
        height: 300px;
        right: 0;
        bottom: 0;
        opacity: 90%;
        background-color: #636363;
        display: flex;
        justify-content: center;
        align-items: center;

        p {
          color: white;
          font-size: 16px;
        }
      }
    }
  }

  .sub-description {
    font-size: 12px;
    color: $defaultTextColor;
    text-align: left;
    margin-left: 26px;
  }

  .power-by {
    text-align: center;
    margin: 10px;
    color: #d2d2d2;
    font-size: 12px;
    display: block;
    //position: absolute;
    //bottom: 10px;
    //width: 100%;

    a {
      color: #d2d2d2;
      font-size: 12px;
      text-decoration: none;
    }
  }
}
</style>
<script lang="ts">
import { Vue, Component, Prop, Watch } from "vue-property-decorator";
import QRCode from "qrcode";
import type { ITarget } from "@tefact/core";
import Page from "@tefact/feature-page";
import Form from "@tefact/feature-form";
import getSharePageLink from "../../utils/getSharePageLink";

@Component({
  components: {
    Form,
    Page,
  },
})
export default class SharePage extends Vue {
  @Prop() addTargetData;
  @Prop() getTargetById;
  @Prop(Boolean) isSharePage!: boolean;
  @Prop(Object) page!: ITarget;
  @Prop(Object) vendor!: Record<string, ITarget>;

  isMobileInDesktop = false;
  link = "";
  qrcode = null;

  get setting() {
    return {
      getTargetByIdHandler: async (id: string) => {
        const vendor = this.vendor[id];
        if (vendor) return vendor;
        return await this.getTargetById(id);
      },
      onFormDataSubmit: this.handleAddTargetData,
    };
  }

  get isMobile() {
    return this.page.displayType !== "page";
  }

  async handleAddTargetData(e) {
    this.$emit("submit", e);
  }

  @Watch("page", { immediate: true })
  async init() {
    if (!this.$el) return false;
    const width = this.$el.getBoundingClientRect().width;
    this.isMobileInDesktop = width > 600 && this.isMobile;

    if (!this.page?.share?.key) return false;

    this.link = this.isSharePage
      ? location.href
      : getSharePageLink(this.page?.share?.key);

    if (this.isMobileInDesktop) {
      this.qrcode = await QRCode.toDataURL(this.link);
    }
  }

  handleCopy() {
    (this as any).$copyText(this.link as string).then(
      () => {
        this.$message.success("复制成功");
      },
      () => {
        this.$message.error("复制失败，请手动复制");
      }
    );
  }

  mounted() {
    this.init();
  }
}
</script>
