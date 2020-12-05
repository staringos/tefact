<template>
  <div :class="`editor-page-canvas ${direction}-side`" :style="style" @click="resetActive">
    <div class="section section-add" v-if="!page.page_section || page.page_section.length < 1" >
      <AddButton :index="0" :pageId="pageId" show></AddButton>
    </div>
    <PageSection
      v-for="(section, i) in page.page_section"
      :key="i"
      :index="i"
      :section="section"
      :pageId="pageId"
      :preview="preview"
      :active="currentPageSectionIdGetter === section.id"
      @onActiveChange="handleActiveChange(section.id)"
    ></PageSection>
  </div>
</template>
<script lang="ts">
  import { Vue, Component, Prop, namespace } from 'nuxt-property-decorator'

  import 'vue-draggable-resizable-gorkys/dist/VueDraggableResizable.css'
  import PageSection from '~/components/app/light/editor/PageSection.vue'
  import { PageModel } from '~/utils/entities/editor/page'
  import AddButton from '~/components/app/light/editor/AddButton.vue'
  import cloneDeep from 'lodash/cloneDeep'

  const editor = namespace('editor')

  @Component({
    components: {
      AddButton,
      PageSection
    }
  })
  export default class Page extends Vue {
    @Prop() pageId!: string
    @Prop() page!: PageModel
    @Prop({ type: String, default: 'pc' }) device
    @Prop(Boolean) preview!: Boolean

    @editor.Action addPageSection
    @editor.Action choosePageSection
    @editor.Action resetActive
    @editor.Action removeActiveNodes
    @editor.Getter currentPageSectionIdGetter

    get direction() {
      return this.page.direction
    }

    get style() {
      const style = cloneDeep(this.page.config?.style) as any
      if (!style) return
      if (this.page.config.viewMode === "fixed") {
        style.width = style.width + 'px'
      }
      return style
    }

    handleActiveChange(active) {
      this.choosePageSection(active)
    }

    handleKeyDown(e) {
      switch(e.key) {
        case 'Backspace':
          if (this.preview) return;
          this.removeActiveNodes()
      }
    }

    mounted() {
      window.addEventListener('keydown', this.handleKeyDown)
    }

    beforeDestroy() {
      window.removeEventListener('keydown', this.handleKeyDown)
    }
  }
</script>

<style lang="scss" scoped>
  @import "../../../../assets/styles/variables";

  .editor-page-canvas {
    width: 95%;
    display: flex;
    flex-direction: column;
    margin: 0 auto;
    box-shadow: 0 2px 4px 0 rgba(0,0,0,.12), 0 0 6px 0 rgba(0,0,0,.04);

    &.column-side {
      overflow-x: hidden;
    }

    &.row-side {
      overflow-y: hidden;
    }

    .section {
      min-height: 300px;
      background-color: white;
    }

    .section-add {
      border: 2px dashed $secondColor;
      display: flex;
      justify-content: center;
      align-items: center;
      height: 300px;
    }
  }
</style>
