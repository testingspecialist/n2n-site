(function(){
  var toggle = document.getElementById('nav-toggle');
  var links  = document.getElementById('nav-links');
  if (toggle && links) {
    toggle.addEventListener('click', function(){
      var open = links.classList.toggle('is-open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    document.addEventListener('click', function(e){
      if (!toggle.contains(e.target) && !links.contains(e.target)) {
        links.classList.remove('is-open');
        toggle.setAttribute('aria-expanded', 'false');
      }
    });
  }
  var form = document.getElementById('contact-form');
  if (form) {
    form.addEventListener('submit', function(e){
      e.preventDefault();
      var btn = form.querySelector('[type=submit]');
      var msg = document.getElementById('form-msg');
      btn.disabled = true; btn.textContent = 'Enviando\u2026';
      var data = {};
      new FormData(form).forEach(function(v,k){ data[k]=v; });
      data['access_key'] = '805e9884-4601-4a15-b3b7-58d507fae8e3';
      data['subject'] = 'Nueva consulta N2N — ' + (data['sector'] || 'sin sector');
      data['from_name'] = 'N2N Contacto';
      fetch('https://api.web3forms.com/submit', {
        method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(data)
      }).then(function(r){ return r.json(); }).then(function(r){
        if(!r.success) throw new Error();
        if(msg){ msg.textContent='Mensaje enviado. Te contactamos en 24\u201348h h\u00e1biles.'; msg.style.color='#2d8a4e'; }
        form.reset();
      }).catch(function(){
        if(msg){ msg.textContent='Error al enviar. Escrib\u00ednos a contacto@n2n.com.ar'; msg.style.color='#c0392b'; }
      }).finally(function(){
        btn.disabled=false; btn.textContent='Enviar consulta';
      });
    });
  }
})();
