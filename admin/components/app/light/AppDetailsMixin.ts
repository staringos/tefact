import { Vue, Component, namespace } from 'nuxt-property-decorator'
import AppDetails from "~/components/app/light/AppDetails.vue"
import MenuList from "~/components/app/light/MenuList.vue"
import PageList from "~/components/app/light/PageList.vue"
import AppDetailsMenu from '~/components/app/light/AppDetailsMenu.vue'

const app = namespace('app')

@Component({
  layout: 'UserAdmin',
  components: {
    AppDetailsMenu,
    AppDetails, MenuList, PageList,
  },
})
export default class AppDetailsMixin extends Vue {
  public id = ''
  public app = {}

  @app.Action public getAppDetails

  public handleRefresh() {
    this.refresh()
  }

  public handleDataChanged() {}

  public async refresh() {
    this.id = this.$route.params.id
    const res = await this.getAppDetails(this.id)
    this.app = res.data.data
  }

  public async mounted() {
    this.refresh()
  }
}
