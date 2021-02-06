import EventEmitter from "eventemitter3";
import cloneDeep from "lodash/clonedeep";
import flatMapDeep from "lodash/flatMapDeep";
import keyBy from "lodash/keyBy";

export type TargetCompileType = "page" | "form";

export interface ITarget {
  id: string;
  title: string;
  compile: TargetCompileType;
  config: ITargetConfig;
}

export interface INodeStyle extends CSSStyleDeclaration {
  h: number;
  w: number;
}

export interface INodeData {
  target: any;
}

export interface ITargetConfig {
  style: INodeStyle;
  data: INodeData;
  children: IBaseNode[];
}

export interface IBaseNode {
  id: string;
  type: string;
  style: INodeStyle;
  data: INodeData;
  children: IBaseNode[];
}

function _flattenNodes(target: ITarget) {
  return keyBy(flatMapDeep(target.config, "children"));
}

/**
 * Tefact engine basic data process class
 *
 * @param type: engine type
 * @param target: edit target
 * @event add: Add a node to outer
 * @event update: target update
 * @event save: target need to save
 */
export default class Engine extends EventEmitter {
  constructor(compile: TargetCompileType, target: ITarget) {
    super();
    this.compile = compile;
    this.target = target;
    this._tmpTarget = cloneDeep(target);
    this._allNodesMap = _flattenNodes(this._tmpTarget);
  }

  compile: TargetCompileType = "page";
  target: ITarget;
  private _tmpTarget: ITarget;
  private _allNodesMap: Record<string, IBaseNode>;

  public add(config: IBaseNode) {
    this._tmpTarget?.config?.children?.push(config);
    this._allNodesMap = _flattenNodes(this._tmpTarget);
    this.emit("add", this._tmpTarget);
  }

  public update(config: IBaseNode) {
    this._allNodesMap[config.id] = config;
    this.emit("update", this._tmpTarget);
  }

  public save() {
    this.emit("save", this._tmpTarget);
  }
}
