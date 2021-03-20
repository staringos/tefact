import { v4 as uuidV4 } from "uuid";

const generateId = (): string => {
  return uuidV4();
}

export default generateId;
