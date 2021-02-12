import EventEmitter from 'eventemitter3'
import { DEFAULT_SETTING } from './constants'
import cloneDeep from 'lodash/cloneDeep'
import { IEngine, ITarget, IBaseNode, EVENT, ISetting } from "@tefact/core";
import set from 'lodash/set'
import findIndex from 'lodash/findIndex'
import { BFS } from "@tefact/utils"
import { Vue } from "vue-property-decorator"
import { generateId } from "@tefact/utils"

function _flattenNodes(target: ITarget) {
  const map = {} as Record<string, IBaseNode>;
  function popAllChildren(cur:Array<IBaseNode>) {
    cur.forEach(cur => {
      map[cur.id] = cur;
      if (cur.children && cur.children.length > 0) {
        popAllChildren(cur.children);
      }
    })
  }

  popAllChildren(target.config.children)
  return map;
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
export default class Engine extends EventEmitter<string, ITarget> implements IEngine {
  private constructor(target?: ITarget, setting: ISetting = DEFAULT_SETTING) {
    super();
    return this.init(target, setting)
  }

  public activeNodeIds: Array<string> = [];
  public target!: ITarget;
  private _targetBackup!: ITarget;
  private _setting: ISetting = DEFAULT_SETTING;
  private _draggingNode: IBaseNode | null = null;
  private _draggingType: string | null = null;
  private _allNodesMap?: Record<string, IBaseNode>;
  private static _engineInstance: null | Engine = null

  get draggingNode(): IBaseNode | null { return this._draggingNode; }
  get draggingType(): string | null { return this._draggingType; }
  get setting(): ISetting { return this._setting; }
  get featureType(): string { return this.target?.featureType || "page"; }
  get isForm() { return this.target?.featureType === "form"; }
  get activatedNode(): IBaseNode | null {
    if (!this._allNodesMap || !this.activeNodeIds) return null;
    return this._allNodesMap[this.activeNodeIds[0]];
  }

  public init(target?: ITarget, setting?: ISetting) {
    if (target) {
      this.target = Vue.observable(cloneDeep(target));
      this._targetBackup = target;
      this._allNodesMap = _flattenNodes(this.target);
    }

    if (setting) {
      this._setting = setting;
    }

    return Vue.observable(this);
  }

  public dragging(node: IBaseNode, type: string) {
    this._draggingNode = node;
    this._draggingType = type;
  }

  public cleanDragging() {
    this._draggingNode = null;
    this._draggingType = null;
  }

  public activeNode(ids: Array<string>) {
    this.activeNodeIds = ids;
  }

  public moreActive(id: string) {
    this.activeNodeIds.push(id);
  }

  public resetActive = () => {
    this.activeNodeIds = [] as Array<string>;
  }

  public add(config: IBaseNode, index = -1) {
    if (!this.target) return;

    const target = cloneDeep(this.target);
    const newNode = cloneDeep(config);
    newNode.id = generateId();

    if (index === -1) {
      target?.config?.children?.push(newNode);
    } else {
      target?.config?.children.splice(index, 0, newNode);
    }
    this._allNodesMap = _flattenNodes(target);
    this.emit(EVENT.ADD, target);
  }

  public addNode(config: IBaseNode, parentId: string | number = -1) {
    if (!this.target) return;
    if (parentId === -1) {
      return this.add(config, -1);
    }
    const newNode = cloneDeep(config);
    newNode.id = generateId();
    const newConfig = this.target?.config;
    BFS(newConfig.children, parentId).addChild(newNode);
    this._allNodesMap = _flattenNodes(this.target);
    this.emit(EVENT.ADD, this.target);
    this.activeNode([newNode.id])
  }

  public update(path: string, value: any) {
    if (!this.target) return
    this.emit(EVENT.UPDATE, set(this.target, path, value));
  }

  public updateNode(config: IBaseNode) {
    if (!this._allNodesMap) return;
    this._allNodesMap[config.id].style = config.style;
    this._allNodesMap[config.id].pos = config.pos;
    this._allNodesMap[config.id].data = config.data;

    this.emit(EVENT.UPDATE_CONFIG, this.target);
  }

  public save() {
    this.emit(EVENT.ADD, this.target);
  }

  public share() {
    this.emit(EVENT.SHARE, this.target);
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
    if (!this.target) return;
    const config = this.target.config;
    if (!config.children) return;
    config.children = BFS(config.children, id).delete() as any;
    this.emit(EVENT.UPDATE, this.target);
  }

  public copyNode(id: string) {
    if (!this.target) return;
    const config = this.target.config;
    if (!config.children) return;
    config.children = BFS(config.children, id).copy() as any;
    this.emit(EVENT.UPDATE, this.target);
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
    const parentNode = this.target?.config?.children?.filter((cur: IBaseNode) => cur.id === parentId)[0];
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
