<template>
  <div class="editor-page-canvas">
    <PageSection
      v-for="(section, i) in sections"
      :section="section"
      :active="active === section.id"
      @onActiveChange="handleActiveChange(section.id)"
      :key="i"
    ></PageSection>
  </div>
</template>
<script lang="ts">
  import { Vue, Component } from 'nuxt-property-decorator'
  import TextNode from './nodes/TextNode.vue'

  import 'vue-draggable-resizable-gorkys/dist/VueDraggableResizable.css'
  import PageSection from '~/components/app/light/editor/PageSection.vue'

  @Component({
    components: {
      PageSection
    }
  })
  export default class AppItem extends Vue {
    active = null

    handleActiveChange(active) {
      this.active = active
    }

    sections = [{
      id: 1,
      nodes: [{
        id: '123',
        type: 'text',
        config: {
          x: 10,
          y: 10,
          w: 100,
          h: 60
        },
        data: {
          text: '这是一段文字'
        }
      }, {
        id: "234",
        type: 'text',
        config: {
          x: 10,
          y: 10,
          w: 200,
          h: 150
        },
        data: {
          text: "这是一段文字"
        }
      }]
    }, {
      id: 2,
      nodes: []
    }]
  }
</script>

<style lang="scss" scoped>
  @import "../../../../assets/styles/variables";

  .editor-page-canvas {
    width: 80%;
    min-height: 500px;
    display: flex;
    flex-direction: column;
    background: white;
    margin: 0 auto;
    box-shadow: 0 2px 4px 0 rgba(0,0,0,.12), 0 0 6px 0 rgba(0,0,0,.04);
  }
</style>
