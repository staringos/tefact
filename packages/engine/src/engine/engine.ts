import EventEmitter from 'eventemitter3'
import { IEngine } from '../../../common/src'
import { DEFAULT_SETTING } from '@/engine/constants'
import cloneDeep from 'lodash/cloneDeep'
import { TargetCompileType, ITarget, IBaseNode, EVENT, ISetting } from '@tefact/common'
import keyBy from 'lodash/keyBy'
import flatMapDeep from 'lodash/flatMapDeep'
import set from 'lodash/set'

function _flattenNodes(target: ITarget) {
  return keyBy(flatMapDeep(target.config, "children"));
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

  compile: TargetCompileType = "page";
  public activeNodeIds: Array<string> = [];
  public target?: ITarget;
  private _setting?: ISetting;
  private _tmpTarget?: ITarget;
  private _allNodesMap?: Record<string, IBaseNode>;
  private static _engineInstance: null | Engine = null

  get setting(): ISetting | undefined {
    return this._setting;
  }

  get feature(): string {
    return this.target?.feature || "page";
  }

  get isForm() {
    return this.target?.feature === "form";
  }

  public init(target?: ITarget, setting?: ISetting) {
    if (target) {
      this.target = target;
      this.compile = target.feature;
      this._tmpTarget = cloneDeep(target);
      this._allNodesMap = _flattenNodes(this._tmpTarget);
    }

    if (setting) {
      this._setting = setting;
    }
  }

  public active(ids: Array<string>) {
    this.activeNodeIds = ids;
  }

  public resetActive() {
    this.activeNodeIds = [];
  }

  public add(config: IBaseNode) {
    if (!this._tmpTarget) return;
    this._tmpTarget?.config?.children?.push(config);
    this._allNodesMap = _flattenNodes(this._tmpTarget);
    this.emit(EVENT.ADD, this._tmpTarget);
  }

  public update(path: string, value: any) {
    if (!this._tmpTarget) return
    this.emit(EVENT.UPDATE, set(this._tmpTarget, path, value));
  }

  public updateConfig(config: IBaseNode) {
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

  changeSetting(setting: ISetting) {
    this._setting = setting;
  }
}
