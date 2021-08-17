function initFreshChat() {
    window.fcWidget.init({
        token: "29b72a28-26c2-4279-81b8-5210fafa6c90",
        host: "https://wchat.freshchat.com",
        locale: "th",
    });
}

function initialize(i, t) {
    var e;
    i.getElementById(t) ? initFreshChat() : ((e = i.createElement("script")).id = t, e.async = !0, e.src = "https://wchat.freshchat.com/js/widget.js", e.onload = initFreshChat, i.head.appendChild(e))
}

function initiateCall() {
    initialize(document, "Freshdesk Messaging-js-sdk")
}
window.addEventListener ? window.addEventListener("load", initiateCall, !1) : window.attachEvent("load", initiateCall, !1);
