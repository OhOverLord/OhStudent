export function jwtDecrypt(token) {
    var base64Url = String(token).split(".")[1];
    var base64 = String(base64Url).replace(/-/g, "+").replace(/_/g, "/");
    var jsonPayload = decodeURIComponent(
      window.atob(base64)
        .split("")
        .map(function(c) {
          return "%" + ("00" + c.charCodeAt(0).toString(16)).slice(-2);
        })
        .join("")
    );
   
    return JSON.parse(jsonPayload);
  }

export function tokenAlive(exp) {
  if (Date.now() >= exp * 1000) {
    return false;
  }
  return true;
}