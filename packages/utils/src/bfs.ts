import generateId from "./generateId";
import cloneDeep from "lodash/cloneDeep";
import { IBaseNode } from "@tefact/core"

type BFSFindResult<T> = {
  index: number;
  target: T | null;
  parent: Array<T>;
}

interface IBFSInstance<T> {
  find(): BFSFindResult<T>;
  delete(): Array<T>;
  addChild(node: IBaseNode): Array<T>;
  copy(): Array<T>;
}

export default function BFS<T extends {
  id: string | number;
  children?: Array<any>
}>(list: Array<T>, id: string | number): IBFSInstance<T> {
  const { index, target, parent } = BFSFind(list, id);

  return {
    addChild(node: IBaseNode) {
      if (!target || !target.children) return list;
      // const newNode = cloneDeep(node);
      // newNode.id = generateId();

      console.log("parent:", parent);
      target.children.push(node as any);
      return list;
    },
    find(): BFSFindResult<T> {
      return { index, target, parent };
    },
    delete() {
      parent.splice(index, 1)
      return list;
    },
    copy() {
      if (!target) return list;
      target.id = generateId();
      parent.push(cloneDeep(target));
      return list;
    }
  } as any
}

function BFSFind<T extends {
  id: string | number;
  children?: Array<any>
}>(list: Array<T>, id: string | number): BFSFindResult<T> {
  if (!list) return list;
  const isDelete = false;
  let index = -1
  let target = null;
  let parent = [] as Array<T>;

  list.forEach((cur, i) => {
    if (cur.id === id) {
      // list.splice(i, 1)
      // isDelete = true;
      index = i;
      target = cur;
      parent = list;
      return;
    }
  })

  if (index !== -1) return { index, target, parent };

  list.forEach(cur => {
    if (cur.children && cur.children.length > 0) {
      const res = BFSFind(cur.children, id);
      if (res.index !== -1) {
        index = res.index;
        target = res.target;
        parent = res.parent;
      }
    }
  });

  return { index, target, parent };
}
