import EventEmitter from 'eventemitter3'
import { DEFAULT_SETTING } from './constants'
import cloneDeep from 'lodash/cloneDeep'
import { IEngine, ITarget, IBaseNode, EVENT, ISetting } from "@tefact/core";
import keyBy from 'lodash/keyBy'
import flatMapDeep from 'lodash/flatMapDeep'
import flattenDeep from 'lodash/flattenDeep'
import set from 'lodash/set'
import findIndex from 'lodash/findIndex'
import { BFS } from "@tefact/utils"

function _flattenNodes(target: ITarget) {
  return keyBy(flatMapDeep([target.config], "children"), "id");
}

/**
 * @description: Tefact engine basic data process class
 *
 * @param type: engine type
 * @param target: edit target
 * @event add: Add a node to outer
 * @event update: target update
 * @event save: target need to save
 */
export default class Engine extends EventEmitter<string, ITarget> implements IEngine{
  private constructor(target?: ITarget, setting: ISetting = DEFAULT_SETTING) {
    super();
    this.init(target, setting)
  }

  public activeNodeIds: Array<string> = [];
  public target?: ITarget;
  private _setting: ISetting = DEFAULT_SETTING;
  private _tmpTarget?: ITarget;
  private _allNodesMap?: Record<string, IBaseNode>;
  private static _engineInstance: null | Engine = null

  get setting(): ISetting { return this._setting; }
  get featureType(): string { return this.target?.featureType || "page"; }
  get isForm() { return this.target?.featureType === "form"; }
  get activatedNode(): IBaseNode | null {
    console.log("this._allNodesMap:", this._allNodesMap);
    if (!this._allNodesMap || !this.activeNodeIds) return null;
    return this._allNodesMap[this.activeNodeIds[0]];
  }

  public init(target?: ITarget, setting?: ISetting) {
    if (target) {
      this.target = target;
      this._tmpTarget = cloneDeep(target);
      this._allNodesMap = _flattenNodes(this._tmpTarget);
    }

    if (setting) {
      this._setting = setting;
    }
  }

  public activeNode(ids: Array<string>) {
    console.log("activeNode11:", ids);
    this.activeNodeIds = ids;
  }

  public moreActive(id: string) {
    this.activeNodeIds.push(id);
  }

  public resetActive = () => {
    this.activeNodeIds = [] as Array<string>;
  }

  public add(config: IBaseNode, index = -1) {
    if (!this._tmpTarget) return;
    if (index === -1) {
      this._tmpTarget?.config?.children?.push(config);
    } else {
      this._tmpTarget?.config?.children.splice(index, 0, config);
    }
    this._allNodesMap = _flattenNodes(this._tmpTarget);
    this.emit(EVENT.ADD, this._tmpTarget);
  }

  public update(path: string, value: any) {
    if (!this._tmpTarget) return
    this.emit(EVENT.UPDATE, set(this._tmpTarget, path, value));
  }

  public updateNode(config: IBaseNode) {
    if (!this._allNodesMap) return
    this._allNodesMap[config.id] = config;
    this.emit(EVENT.UPDATE_CONFIG, this._tmpTarget);
  }

  public save() {
    this.emit(EVENT.ADD, this._tmpTarget);
  }

  public share() {
    this.emit(EVENT.SHARE, this._tmpTarget);
  }

  public static instance(target?: ITarget, setting: ISetting = DEFAULT_SETTING): Engine {
    if (!Engine._engineInstance) {
      Engine._engineInstance = new Engine(target, setting)
    } else {
      if (target && target !== Engine._engineInstance.target
        || setting && setting !== Engine._engineInstance.setting) {
        Engine._engineInstance.init(target, setting);
      }
    }

    return Engine._engineInstance;
  }

  public changeSetting(setting: ISetting) {
    this._setting = setting;
  }

  public deleteNode(id: string) {
    if (!this._tmpTarget) return;
    const config = this._tmpTarget.config;
    if (!config.children) return;
    config.children = BFS(config.children, id).delete() as any;
    this.emit(EVENT.UPDATE, this._tmpTarget);
  }

  public copyNode(id: string) {
    if (!this._tmpTarget) return;
    const config = this._tmpTarget.config;
    if (!config.children) return;
    config.children = BFS(config.children, id).copy() as any;
    this.emit(EVENT.UPDATE, this._tmpTarget);
  }

  public openTargetEditor(targetId: string) {
    this.emit(EVENT.OPEN_FORM_EDITOR, targetId);
  }

  public toAddTarget() {
    this.emit(EVENT.TO_ADD_TARGET);
  }

  public resetNodeOrder(nodeId: string, index: number) {
    // TODO reset node order
  }

  public reOrderNode(nodeId: string, parentId: string, type: string) {
    const parentNode = this._tmpTarget?.config?.children?.filter((cur: IBaseNode) => cur.id === parentId)[0];
    if (!parentNode) return
    const nodes = parentNode.children
    let index = 0
    let tmp = null as any
    let newList = [] as any

    if (!nodes || nodes.length < 1) return;

    switch(type) {
      case 'top':
        newList = nodes.filter((cur: IBaseNode) => {
          if (cur.id === nodeId) {
            tmp = cur
            return false
          }
          return true
        })
        parentNode.children = [ ...newList, tmp ]
        break
      case 'bottom':
        newList = nodes.filter((cur: IBaseNode) => {
          if (cur.id === nodeId) {
            tmp = cur
            return false
          }
          return true
        })
        parentNode.children = [ tmp, ...newList ]
        break
      case 'up':
        index = findIndex(nodes, (cur: IBaseNode) => cur.id === nodeId);
        if (index >= nodes.length - 1) return
        tmp = nodes[index + 1]
        nodes[index + 1] = nodes[index]
        nodes[index] = tmp
        break
      case 'down':
        index = findIndex(nodes, (cur: IBaseNode) => cur.id === nodeId);
        if (index <= 0) return
        tmp = nodes[index - 1]
        nodes[index - 1] = nodes[index]
        nodes[index] = tmp
        break
    }
  }
}

// type TreeNode = {
//   id: string | number;
//   children?: Array<any>
// }
