<template>
  <div class="editor-page-canvas">
    <div class="section section-add" v-if="!page.page_section || page.page_section.length < 1" >
      <AddButton :index="0" :pageId="pageId" show></AddButton>
    </div>
    <PageSection
      v-for="(section, i) in page.page_section"
      :section="section"
      :pageId="pageId"
      :active="currentPageSectionIdGetter === section.id"
      @onActiveChange="handleActiveChange(section.id)"
      :key="i"
      :index="i"
    ></PageSection>
  </div>
</template>
<script lang="ts">
  import { Vue, Component, Prop, namespace } from 'nuxt-property-decorator'
  import TextNode from './nodes/TextNode.vue'

  import 'vue-draggable-resizable-gorkys/dist/VueDraggableResizable.css'
  import PageSection from '~/components/app/light/editor/PageSection.vue'
  import { PageModel } from "~/utils/entities/editor/page";
  import AddButton from "~/components/app/light/editor/AddButton.vue"

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
    @editor.Action addPageSection
    @editor.Action choosePageSection
    @editor.Action resetActive
    @editor.Getter currentPageSectionIdGetter

    handleActiveChange(active) {
      this.choosePageSection(active)
    }
  }
</script>

<style lang="scss" scoped>
  @import "../../../../assets/styles/variables";

  .editor-page-canvas {
    width: 80%;
    display: flex;
    flex-direction: column;
    margin: 0 auto;
    box-shadow: 0 2px 4px 0 rgba(0,0,0,.12), 0 0 6px 0 rgba(0,0,0,.04);

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
