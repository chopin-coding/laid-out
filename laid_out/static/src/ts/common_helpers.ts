export function getCurrentBaseUrl(): string {
  // Get the current URL
  const currentUrl = window.location.href;

  // Use URL constructor to extract the base URL
  const url = new URL(currentUrl);
  let baseUrl = url.origin;
  return baseUrl
}
