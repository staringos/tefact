<template>
  <BaseProperties title="背景设置" v-bind="$attrs">
    <div class="resolu-container" v-if="tmpNode">
      <div class="resolu-row">
        <div class="resolu-label">背景色</div>
        <el-color-picker
          v-model="tmpNode.style['background-color']"
          @change="handleSave"
          show-alpha
        ></el-color-picker>
      </div>
      <div class="resolu-row">
        <div class="resolu-label">背景图</div>
        <image-uploader v-model="tmpInput" />
        <el-button
          v-if="tmpInput"
          type="text"
          icon="el-icon-delete"
          @click="handleDeleteBackground"
        ></el-button>
      </div>
    </div>
  </BaseProperties>
</template>
<style lang="scss">
@import "./properties.scss";
</style>
<script lang="ts">
import { Component, Watch } from "vue-property-decorator";
import BaseProperties from "./Base.vue";
import PropertiesMixin from "../components/PropertiesMixin";
import PropertiesClass from "../components/PropertiesClass";
import { ImageUploader } from "@tefact/ui";

@Component({
  components: {
    ImageUploader,
    BaseProperties,
  },
  mixins: [PropertiesMixin],
})
export default class Background extends PropertiesClass {
  tmpInput: string | null = null;

  @Watch("tmpNode", { immediate: true, deep: true })
  handleTmpNodeChange() {
    if (!this.tmpNode) return;
    console.log("tmpNode:", this.tmpNode);
    const image = (this as any).tmpNode.style["background-image"];
    if (!image) {
      this.tmpInput = null;
      return;
    }
    this.tmpInput = image.substr(4, image.lastIndexOf(")") - 4);
  }

  @Watch("tmpInput")
  handleUpdate() {
    if (!this.tmpInput) return;
    const style = (this as any).tmpNode.style;
    style["background-image"] = `url(${this.tmpInput})`;
    style["background-size"] = `100% 100%`;
    this.handleSave();
  }

  handleDeleteBackground() {
    const style = (this as any).tmpNode.style;

    delete style["background-image"];
    delete style["background-size"];
    this.handleSave();
  }
}
</script>
