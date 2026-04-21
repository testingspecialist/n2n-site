(function(){
  // ---- Mobile nav ----
  var toggle = document.getElementById('nav-toggle');
  var links  = document.getElementById('nav-links');

  function closeNav(){
    if (!links || !toggle) return;
    links.classList.remove('is-open');
    toggle.setAttribute('aria-expanded', 'false');
  }

  if (toggle && links) {
    toggle.addEventListener('click', function(){
      var open = links.classList.toggle('is-open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    document.addEventListener('click', function(e){
      if (!toggle.contains(e.target) && !links.contains(e.target)) closeNav();
    });
    document.addEventListener('keydown', function(e){
      if (e.key === 'Escape' && links.classList.contains('is-open')) {
        closeNav();
        toggle.focus();
      }
    });
    var mql = window.matchMedia('(min-width: 641px)');
    (mql.addEventListener ? mql.addEventListener.bind(mql, 'change') : mql.addListener.bind(mql))(function(e){
      if (e.matches) closeNav();
    });
    links.addEventListener('click', function(e){
      if (e.target.closest('a')) closeNav();
    });
  }

  // ---- Contact form ----
  var form = document.getElementById('contact-form');
  if (!form) return;

  var EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;

  function setMsg(msg, text, kind){
    if (!msg) return;
    msg.textContent = text;
    msg.style.color = kind === 'ok' ? '#2d8a4e' : (kind === 'err' ? '#c0392b' : '');
    msg.setAttribute('role', kind === 'err' ? 'alert' : 'status');
  }

  function validate(data){
    if (!data.name || data.name.trim().length < 3) return 'Ingresá tu nombre y empresa (mínimo 3 caracteres).';
    if (!EMAIL_RE.test(data.email || '')) return 'Email corporativo inválido.';
    if (!data.sector) return 'Seleccioná un sector.';
    if (!data.problem || data.problem.trim().length < 20) return 'Contanos el problema con un poco más de detalle (mínimo 20 caracteres).';
    if ((data.problem || '').length > 2000) return 'El texto del problema supera los 2000 caracteres.';
    return null;
  }

  form.addEventListener('submit', function(e){
    e.preventDefault();
    var btn = form.querySelector('[type=submit]');
    var msg = document.getElementById('form-msg');

    var data = {};
    new FormData(form).forEach(function(v,k){ data[k] = typeof v === 'string' ? v : ''; });

    var err = validate(data);
    if (err) { setMsg(msg, err, 'err'); return; }

    btn.disabled = true;
    var originalLabel = btn.textContent;
    btn.textContent = 'Enviando\u2026';
    setMsg(msg, '', null);

    data['access_key'] = '805e9884-4601-4a15-b3b7-58d507fae8e3';
    data['subject']    = 'Nueva consulta N2N \u2014 ' + (data['sector'] || 'sin sector');
    data['from_name']  = 'N2N Contacto';

    var ctrl = ('AbortController' in window) ? new AbortController() : null;
    var timeoutId = setTimeout(function(){ if (ctrl) ctrl.abort(); }, 15000);

    fetch('https://api.web3forms.com/submit', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
      body: JSON.stringify(data),
      signal: ctrl ? ctrl.signal : undefined
    })
      .then(function(r){
        return r.json().catch(function(){ return { success:false, status:r.status }; })
          .then(function(body){ return { ok:r.ok, status:r.status, body:body }; });
      })
      .then(function(res){
        if (res.body && res.body.success) {
          setMsg(msg, 'Mensaje enviado. Te contactamos en 24\u201348h h\u00e1biles.', 'ok');
          form.reset();
          return;
        }
        if (res.status === 429) throw new Error('rate');
        if (res.status >= 500)  throw new Error('server');
        if (res.status >= 400)  throw new Error('client');
        throw new Error('unknown');
      })
      .catch(function(e){
        var text;
        if (e && e.name === 'AbortError')          text = 'La conexi\u00f3n tard\u00f3 demasiado. Revis\u00e1 tu red e intent\u00e1 de nuevo, o escrib\u00ednos a contacto@n2n.com.ar.';
        else if (e && e.message === 'rate')        text = 'Demasiados intentos. Esper\u00e1 un momento y volv\u00e9 a intentar.';
        else if (e && e.message === 'server')      text = 'El servicio est\u00e1 ca\u00eddo. Escrib\u00ednos a contacto@n2n.com.ar.';
        else if (e && e.message === 'client')      text = 'Hubo un problema con los datos enviados. Revis\u00e1 el formulario o escrib\u00ednos a contacto@n2n.com.ar.';
        else                                        text = 'Error al enviar. Escrib\u00ednos a contacto@n2n.com.ar.';
        setMsg(msg, text, 'err');
      })
      .then(function(){
        clearTimeout(timeoutId);
        btn.disabled = false;
        btn.textContent = originalLabel;
      });
  });
})();