#!/usr/bin/env node

const config = require('../arrplat.config.json')
const { Builder } = require( '@arrplat/core')
const { ArrplatConfig } = require('@arrplat/common')

const gradient = require('gradient-string')

// TODO
// 1. init build
//    - plugins
//        - pages
//        - store
//        - middleware
// 2. write config files
function main() {
// Works with aliases
//   gradient.atlas.multiline('Multi line\nstring');

// Works with advanced options
  gradient('cyan', 'pink').multiline('Multi line\nstring', {interpolation: 'hsv'});

  const { log } = console
  const title = '   	Arrplat'
  const str = '   	The PaaS Framework for Enterprise'

  log(gradient.pastel.multiline(title));
  log(gradient['atlas'](str) + '\n');

  return Builder.build(config)
}

main().then(() => {
  console.log('success')
}).catch(e => {
  console.log('error:', e)
})
