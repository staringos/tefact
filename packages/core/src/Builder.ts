import Arrplat from './Arrplat'
import { ArrplatConfig, ArrplusConfig } from '@arrplat/common'
import ArrplusFactory from './ArrplusFactory'

const DefaultConfig = {
  name: 'Arrplat',
  description: 'The best ',
  plus: {
    ...ArrplusFactory._defaultConfig,
  },

} as ArrplatConfig

export default class Builder {
  constructor(config: ArrplatConfig) {
    this.config = {
      ...this.config,
      ...config,
    }
  }

  public arrplat!: Arrplat
  public config: ArrplatConfig = DefaultConfig
  public static builder: Builder

  /**
   * Get all arrplus's configuration
   * @param config
   */
  public static async generateOptions(config: ArrplatConfig) {
    this.builder = new Builder(config)
    this.builder.arrplat = await Arrplat.init(config)
    return this.builder.arrplat.generateOptions()
  }

  /**
   * Collect all arrplus's configuration and generate them to .arrplat.json
   * @param config
   */
  public static async build(config: ArrplatConfig) {
    const fs = require('fs-extra')
    const options = await this.generateOptions(config)
    fs.writeFile('.arrplat.json', JSON.stringify(options), (err) => {
      err && console.log('Write file error...:', err)
    })

    return options
  }

  public static async updateArrplus(key: string, config: ArrplusConfig) {

  }
}
