import EventEmitter from 'eventemitter3'
import { DEFAULT_SETTING } from './constants'
import cloneDeep from 'lodash/cloneDeep'
import type { IEngine, ITarget, IBaseNode, ISetting } from "@tefact/core";
import { EVENT } from "@tefact/core";
import set from 'lodash/set'
import findIndex from 'lodash/findIndex'
import merge from "lodash/merge"
import { BFS } from "@tefact/utils"
import { Vue } from "vue-property-decorator"
import { generateId } from "@tefact/utils"
import { INodeStyle, IPos, ShareDataType, TargetDisplayType } from "../types"
import { DefaultTarget } from "../constants"

type IFlattenNode = {
  parentId?: string | number
} & IBaseNode;

function _flattenNodes(target: ITarget) {
  const map = {} as Record<string, IFlattenNode>;
  function popAllChildren(parent:Array<IFlattenNode>, parentId: number | string = -1) {
    parent.forEach((cur) => {
      cur.parentId = parentId
      map[cur.id] = cur;
      if (cur.children && cur.children.length > 0) {
        popAllChildren(cur.children, cur.id);
      }
    })
  }

  popAllChildren(target.config.children as Array<IFlattenNode>)
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
    return this.init(target, setting);
  }

  public activeNodeIds: Array<string> = [];
  public target!: ITarget;
  public setting: ISetting = Vue.observable(DEFAULT_SETTING);

  private _targetBackup!: ITarget;
  private _draggingNode: IBaseNode | null = null;
  private _draggingType: string | null = null;
  private _allNodesMap?: Record<string, IFlattenNode>;
  private static _engineInstance: null | Engine = null

  get draggingNode(): IBaseNode | null { return this._draggingNode; }
  get draggingType(): string | null { return this._draggingType; }
  get featureType(): string { return this.target?.featureType || "page"; }
  get isForm() { return this.target?.featureType === "form"; }
  get activatedNode(): IFlattenNode | null {
    if (!this._allNodesMap || !this.activeNodeIds) return null;
    return this._allNodesMap[this.activeNodeIds[0]];
  }
  get activatedNodeParentId(): string | number | undefined {
    if (!this.activatedNode) return -1;
    return this.activatedNode.parentId;
  }

  public init(target?: ITarget, setting?: ISetting) {
    if (!target) return this;
    let mergedTarget = merge(DefaultTarget, target);

    Vue.set(this, "target", Vue.observable(cloneDeep(mergedTarget)));
    this._targetBackup = mergedTarget;
    this._refreshAllNodeMap();

    if (mergedTarget || this.target) {
      const displayType = (mergedTarget || this.target).displayType;
      if (setting && displayType) this.changeSetting(displayType, setting);
    }
    return this;
  }

  private _refreshAllNodeMap() {
    this._allNodesMap = _flattenNodes(this.target);
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

  public resetActive() {
    this.activeNodeIds = [];
  }

  public replaceChildren(children: Array<IBaseNode>) {
    Vue.set(this.target.config, "children", children);
    this.emit(EVENT.UPDATE, this.target);
  }

  public add(config: IBaseNode, index = -1) {
    if (!this.target) return;

    const target = this.target;
    const newNode = cloneDeep(config);
    newNode.id = generateId();

    if (index === -1) {
      target?.config?.children?.push(newNode);
    } else {
      target?.config?.children.splice(index, 0, newNode);
    }
    this._refreshAllNodeMap()
    this.emit(EVENT.ADD, target);
  }

  public addNode(config: IBaseNode, parentId: string | number = -1) {
    if (!this.target) return;
    const newNode = cloneDeep(config);
    newNode.id = generateId();
    const newConfig = this.target?.config;

    if (parentId === -1) parentId = newConfig.children[0].id
    BFS(newConfig.children, parentId).addChild(newNode);
    this._refreshAllNodeMap();
    this.emit(EVENT.ADD, this.target);
    this.activeNode([newNode.id])
  }

  public addSlot(name: string, config: IBaseNode) {
    if (!this.target) return;
    const newNode = cloneDeep(config);
    newNode.id = generateId();
    newNode.slotName = name;
    const newConfig = this.target?.config;

    Vue.set(newConfig.slots, name, newNode);
    this.emit(EVENT.ADD, this.target);

    this.activeNode([newNode.id])
  }

  public update(path: string, value: any) {
    if (!this.target) return
    this.emit(EVENT.UPDATE, set(this.target, path, value));
  }

  public updateNode(config: any) {
    if (!this._allNodesMap) return;
    const isPage = config.config && config.featureType;

    let oldTarget;

    // modify page config
    if (isPage) {
      oldTarget = this.target.config;
    } else {
      oldTarget = this._allNodesMap[config.id] as Record<string, any>;
    }

    const newConfig = isPage ? config.config : config;

    for (let key in newConfig) {
      if (newConfig.hasOwnProperty(key)) {
        oldTarget[key] = (newConfig as Record<string, any>)[key] as any;
      }
    }

    // this._allNodesMap[config.id].style = config.style;
    // this._allNodesMap[config.id].pos = config.pos;
    // this._allNodesMap[config.id].data = config.data;

    this.emit(EVENT.UPDATE_CONFIG, this.target);
  }

  public updateNodePos(id: string, pos: IPos) {
    if (!this._allNodesMap) return;
    this._allNodesMap[id].pos = pos;
    this.emit(EVENT.UPDATE_CONFIG, this.target);
  }

  public updateNodeStyle(id: string, style: INodeStyle) {
    if (!this._allNodesMap) return;
    this._allNodesMap[id].style = style;
    this.emit(EVENT.UPDATE_CONFIG, this.target);
  }

  public updateNodeData(id: string, data: any) {
    if (!this._allNodesMap) return;
    this._allNodesMap[id].data = data;
    this.emit(EVENT.UPDATE_CONFIG, this.target);
  }

  public save() {
    this.emit(EVENT.SAVE, this.target);
  }

  public share(shareData: ShareDataType) {
    return this.setting.onShare(shareData);
  }

  public cancelShare() {
    return this.emit(EVENT.SHARE_CANCEL, this.target.id);
  }

  public static instance(target?: ITarget, setting: ISetting = DEFAULT_SETTING): Engine {
    if (!Engine._engineInstance) {
      Engine._engineInstance = Vue.observable(new Engine(target, setting)) as Engine;
    } else {
      if (target && target !== Engine._engineInstance.target
        || setting && setting !== Engine._engineInstance.setting) {
        Engine._engineInstance.init(target, setting);
      }
    }

    return Engine._engineInstance;
  }

  public changeSettingItem(key: string, value: any) {
    Vue.set(this.setting, key, value);
  }

  public changeSetting(displayType: TargetDisplayType | null, setting: ISetting) {
    const tmpSetting = Vue.observable(merge(DEFAULT_SETTING, setting));
    if (displayType) {
      tmpSetting.device = displayType !== "page" ? "mobile" : "pc";
    }
    this.setting = tmpSetting;
    return this.setting;
  }

  public moveNode(nodeId: string, newParentId: string) {
    if (!this.target) return;
    const config = this.target.config;
    if (!config.children) return;
    config.children = BFS(config.children, nodeId).move(newParentId) as any;
    this.emit(EVENT.UPDATE, this.target);
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

  public targetEdit(targetId: string) {
    this.emit(EVENT.EDIT_TARGET, targetId);
  }

  public targetAdd() {
    this.emit(EVENT.ADD_TARGET);
  }

  public resetNodeOrder(nodeId: string, index: number) {
    if (!this._allNodesMap) return;
    const node = this._allNodesMap[nodeId];
    const newChildren = [] as Array<IBaseNode>;
    const children = this.target?.config?.children;

    let before = false;
    children.forEach((cur: IBaseNode, i: number) => {
      if (cur.id === node.id) {
        before = i < index;
        return;
      }
      if (i === index) {
        if (before) newChildren.push(cur);
        newChildren.push(node);
        if (!before) newChildren.push(cur);
        return;
      }
      newChildren.push(cur);
    });
    Vue.set(this.target?.config, "children", newChildren);
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

  getTargetById(id: string): Promise<ITarget> | null {
    if (!this.setting.getTargetByIdHandler) {
      return null;
    }

    return this.setting.getTargetByIdHandler(id);
  }

  public openModify() {
    this.emit(EVENT.OPEN_MODIFIER, this.target);
  }

  public back() {
    this.emit(EVENT.BACK);
  }
}
