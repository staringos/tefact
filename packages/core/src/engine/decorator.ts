import Vue from "vue";
import { IEngine } from "@tefact/core";
import Engine from './index';

type DecoratorOption = {};

export type VueClass<V> = { new (...args: any[]): V & Vue } & typeof Vue;

export type TVue = Vue & { $engine: IEngine };

export function Combine <VC extends Vue>(target: VC): TVue {
  const tmp = { $engine: Engine.instance() }
  return Object.assign(target, tmp);
}
