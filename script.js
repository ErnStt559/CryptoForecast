 <!-- Cookie Consent Banner -->
<div id="cookie-consent" style="
  position: fixed;
  bottom: 0;
  left: 0;
  width: 100%;
  background: #000;
  color: #00ff00;
  padding: 15px;
  font-family: Arial, sans-serif;
  text-align: center;
  z-index: 9999;
  border-top: 1px solid #00ff00;
">
  This site uses cookies for advertising. Please accept to continue.
  <button onclick="acceptCookies()" style="
    margin-left: 10px;
    background: transparent;
    border: 1px solid #00ff00;
    color: #00ff00;
    padding: 5px 15px;
    cursor: pointer;
  ">Accept</button>
</div>

<script>
function acceptCookies() {
  document.getElementById("cookie-consent").style.display = "none";
  localStorage.setItem("cookiesAccepted", "true");

  // Загружаем рекламу AdSense после согласия
  var adsScript = document.createElement("script");
  adsScript.async = true;
  adsScript.src = "https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js";
  adsScript.setAttribute("data-ad-client", "ca-pub-XXXXXXXXXXXXXXX"); // <-- сюда вставь свой Publisher ID
  document.head.appendChild(adsScript);
}

window.onload = function() {
  if (!localStorage.getItem("cookiesAccepted")) {
    document.getElementById("cookie-consent").style.display = "block";
  } else {
    acceptCookies(); // Если согласие уже было — сразу загружаем рекламу
  }
}
</script>
