import { ArrplusConfig, ArrplusOptions } from './arrplus'

export interface ArrplatConfig {
  name?: string
  description?: string
  plus: ArrplusConfig
}

// Entity build by builder which is global options use by both python & ts side
export interface ArrplatOptions {
  name?: string
  description?: string
  plus: ArrplusOptions,
}
