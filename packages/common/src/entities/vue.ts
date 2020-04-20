type Dictionary < T > = { [key: string]: T }

export interface Route {
  path: string
  name?: string
  hash: string
  query: Dictionary<string | (string | null)[]>
  params: Dictionary<string>
  fullPath: string
  matched: any[]
  redirectedFrom?: string
  meta?: any
}
