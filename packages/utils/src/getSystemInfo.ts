export default function getSystemInfo() {
  return {
    appCodeName: navigator.appCodeName,
    appName: navigator.appName,
    cookieEnabled: navigator.cookieEnabled,
    language: navigator.language,
    onLine: navigator.onLine,
    platform: navigator.platform,
    appVersion: navigator.appVersion
  }
};
