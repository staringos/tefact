export default function hasMetaKeyPass() {
  return window && window.event && ((window.event as any)['ctrlKey'] || (window.event as any)['metaKey'])
}
