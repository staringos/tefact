function getSharePageLink(key: string | undefined) {
  const host = window.location.host;
  const protocol = window.location.protocol;
  return `${protocol}//${host}/s/p/${key}`;
}

export default getSharePageLink
