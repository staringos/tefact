import { v4 as uuidV4 } from "uuid";

const generateId = (): string => {
  return uuidV4() // Generate node id
}

export default generateId;
