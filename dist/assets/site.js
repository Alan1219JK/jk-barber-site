/* J&K Barber Shop, j-kbarber.no. Ingen avhengigheter. Lastes med defer.
   1) mobilmeny  2) sticky bunn-CTA  3) dataLayer-push på bestill-klikk  4) skjema til Wix Forms  5) ?avd= forhåndsvalg */
(function () {
  "use strict";

  var WIX_CLIENT_ID = "dbd18313-acf6-4a35-b6e3-11b05b4d0914";
  var WIX_API = "https://www.wixapis.com";
  var TOKEN_KEY = "wix-visitor-" + WIX_CLIENT_ID;

  /* ---------- 1. Mobilmeny ---------- */
  var knapp = document.querySelector(".meny-knapp");
  var nav = document.getElementById("hovedmeny");
  if (knapp && nav) {
    function lukk() {
      nav.classList.remove("apen");
      knapp.setAttribute("aria-expanded", "false");
      document.body.classList.remove("meny-apen");
    }
    knapp.addEventListener("click", function () {
      var apen = nav.classList.toggle("apen");
      knapp.setAttribute("aria-expanded", apen ? "true" : "false");
      document.body.classList.toggle("meny-apen", apen);
    });
    document.addEventListener("keydown", function (ev) {
      if (ev.key === "Escape" && nav.classList.contains("apen")) { lukk(); knapp.focus(); }
    });
    window.addEventListener("resize", function () {
      if (window.innerWidth >= 1080) lukk();
    });
  }

  /* ---------- 2. Sticky CTA på mobil etter 300 px scroll ---------- */
  var sticky = document.getElementById("sticky-cta");
  if (sticky) {
    var ticking = false;
    function oppdater() {
      ticking = false;
      var vis = window.scrollY > 300 && window.innerWidth < 1080;
      sticky.classList.toggle("vis", vis);
    }
    window.addEventListener("scroll", function () {
      if (!ticking) { ticking = true; window.requestAnimationFrame(oppdater); }
    }, { passive: true });
    window.addEventListener("resize", oppdater);
    oppdater();
  }

  /* ---------- 3. dataLayer-push på bestill-klikk ---------- */
  window.dataLayer = window.dataLayer || [];
  document.addEventListener("click", function (ev) {
    var a = ev.target.closest ? ev.target.closest("a[data-bestill]") : null;
    if (!a) return;
    window.dataLayer.push({
      event: "bestill_klikk",
      avdeling: a.getAttribute("data-bestill") || "felles",
      plassering: a.getAttribute("data-plassering") || "",
      side: location.pathname,
      lenke: a.getAttribute("href")
    });
  });

  /* ---------- 4. Skjema til Wix Forms ----------
     <form data-wix-form="<formId>" data-takk="#takk-id"> med felt der name = feltets target i Wix.
     Checkbox sendes som boolean, checkbox-gruppe (flere med samme name) som liste, date som YYYY-MM-DD,
     tel normaliseres til E.164 (+47 som standard). */
  function hentToken() {
    var lagret = null;
    try { lagret = JSON.parse(localStorage.getItem(TOKEN_KEY)); } catch (e) { lagret = null; }
    if (lagret && lagret.expiresAt - 60000 > Date.now()) return Promise.resolve(lagret.accessToken);
    function mint(body) {
      return fetch(WIX_API + "/oauth2/token", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(Object.assign({ clientId: WIX_CLIENT_ID }, body))
      }).then(function (r) {
        if (!r.ok) throw new Error("Wix auth " + r.status);
        return r.json();
      }).then(function (d) {
        var t = { accessToken: d.access_token, refreshToken: d.refresh_token, expiresAt: Date.now() + d.expires_in * 1000 };
        try { localStorage.setItem(TOKEN_KEY, JSON.stringify(t)); } catch (e) { /* privat modus */ }
        return t.accessToken;
      });
    }
    var p = Promise.reject();
    if (lagret && lagret.refreshToken) p = mint({ grantType: "refresh_token", refreshToken: lagret.refreshToken });
    return p.catch(function () { return mint({ grantType: "anonymous" }); });
  }

  function e164(v) {
    var s = (v || "").replace(/[\s().-]/g, "");
    if (!s) return "";
    if (s.indexOf("00") === 0) s = "+" + s.slice(2);
    if (s[0] !== "+") s = "+47" + s;
    return s;
  }

  function samleVerdier(form) {
    var data = {};
    var felter = form.querySelectorAll("[name]");
    Array.prototype.forEach.call(felter, function (f) {
      if (f.disabled || !f.name || f.type === "submit" || f.type === "button") return;
      var n = f.name;
      if (f.type === "checkbox") {
        var gruppe = form.querySelectorAll('input[type=checkbox][name="' + n + '"]');
        if (gruppe.length > 1) {
          data[n] = Array.prototype.filter.call(gruppe, function (g) { return g.checked; }).map(function (g) { return g.value; });
        } else {
          data[n] = f.checked;
        }
      } else if (f.type === "radio") {
        if (f.checked) data[n] = f.value;
        else if (!(n in data)) data[n] = data[n];
      } else if (f.type === "tel") {
        data[n] = e164(f.value);
      } else {
        data[n] = f.value.trim();
      }
    });
    Object.keys(data).forEach(function (k) {
      if (data[k] === "" || data[k] === undefined) delete data[k];
    });
    return data;
  }

  function sett(form, msg, feil) {
    var st = form.querySelector(".skjema-status");
    if (!st) return;
    st.textContent = msg || "";
    st.classList.toggle("feil", !!feil);
  }

  function validerKlient(form) {
    var ok = true;
    Array.prototype.forEach.call(form.querySelectorAll(".felt"), function (felt) {
      felt.classList.remove("ugyldig");
      var inp = felt.querySelector("input,select,textarea");
      if (inp && !inp.checkValidity()) { felt.classList.add("ugyldig"); ok = false; }
    });
    return ok && form.checkValidity();
  }

  Array.prototype.forEach.call(document.querySelectorAll("form[data-wix-form]"), function (form) {
    form.setAttribute("novalidate", "novalidate");
    form.addEventListener("submit", function (ev) {
      ev.preventDefault();
      if (!validerKlient(form)) {
        sett(form, "Fyll ut feltene som er merket, så prøver vi igjen.", true);
        var f1 = form.querySelector(".ugyldig input,.ugyldig select,.ugyldig textarea,:invalid");
        if (f1) f1.focus();
        return;
      }
      var knapp = form.querySelector('button[type=submit]');
      var gammel = knapp ? knapp.textContent : "";
      if (knapp) { knapp.disabled = true; knapp.textContent = "Sender ..."; }
      sett(form, "");
      var body = { submission: { formId: form.getAttribute("data-wix-form"), submissions: samleVerdier(form) } };
      hentToken().then(function (token) {
        return fetch(WIX_API + "/form-submission-service/v4/submissions", {
          method: "POST",
          headers: { Authorization: token, "Content-Type": "application/json" },
          body: JSON.stringify(body)
        });
      }).then(function (r) {
        if (r.status === 400) {
          return r.json().then(function (d) {
            var v = d && d.details && d.details.validationError && d.details.validationError.fieldViolations;
            var tekst = v && v.length ? "Sjekk feltet " + (v[0].field || "") + ". " : "";
            throw new Error(tekst + "Skjemaet ble ikke sendt.");
          });
        }
        if (!r.ok) throw new Error("Skjemaet ble ikke sendt (" + r.status + ").");
        return r.json();
      }).then(function () {
        form.classList.add("sendt");
        var takk = document.querySelector(form.getAttribute("data-takk") || ".skjema-takk");
        if (takk) { takk.style.display = "block"; takk.setAttribute("tabindex", "-1"); takk.focus(); }
        window.dataLayer.push({ event: "skjema_sendt", skjema: form.getAttribute("data-skjema") || form.getAttribute("data-wix-form"), side: location.pathname });
      }).catch(function (err) {
        sett(form, (err && err.message ? err.message : "Noe gikk galt.") + " Prøv igjen, eller send e-post til post@j-kbarber.no.", true);
        if (knapp) { knapp.disabled = false; knapp.textContent = gammel; }
      });
    });
  });

  /* ---------- 5. ?avd=<slug> forhåndsvelger avdeling i nedtrekk og markerer knapp ---------- */
  try {
    var avd = new URLSearchParams(location.search).get("avd");
    if (avd) {
      Array.prototype.forEach.call(document.querySelectorAll("select[data-avd-velger]"), function (sel) {
        Array.prototype.forEach.call(sel.options, function (o) {
          if (o.getAttribute("data-slug") === avd) sel.value = o.value;
        });
      });
      var mal = document.querySelector('[data-avd-kort="' + avd + '"]');
      if (mal) mal.classList.add("niva-senior");
    }
  } catch (e) { /* ignorer */ }
})();
