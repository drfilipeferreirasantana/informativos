// Conta as visitas e reconhece no sistema do escritório quem chamou no WhatsApp
// pelo site de informativos. Não guarda nem envia nome, telefone, IP ou cookie.
(function () {
  var SISTEMA = 'https://sistema.filipeferreiraadv.com/api/public/site/';
  var NUMERO = 'https://wa.me/5527995187279';
  var GERAL = 'Olá! Vim pelo site de informativos e gostaria de falar com o escritório.';
  var ALFABETO = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789';

  function enviar(rota, dados) {
    try {
      fetch(SISTEMA + rota, {
        method: 'POST', mode: 'no-cors', keepalive: true, headers: { 'Content-Type': 'text/plain' },
        body: JSON.stringify(dados)
      }).catch(function () {});
    } catch (e) { /* sem registro: o site funciona do mesmo jeito */ }
  }

  // De onde veio a visita (a primeira página da visita decide)
  function lerOrigem() {
    var q = new URLSearchParams(location.search);
    var fonte = (q.get('utm_source') || '').toLowerCase();
    var host = '';
    try { host = document.referrer ? new URL(document.referrer).hostname : ''; } catch (e) { host = ''; }
    if (host === location.hostname) host = '';
    var origem = 'direto';
    if (q.get('gclid') || (fonte.indexOf('google') >= 0 && /cpc|ads|paid/.test((q.get('utm_medium') || '').toLowerCase()))) origem = 'google_ads';
    else if (fonte.indexOf('instagram') >= 0 || host.indexOf('instagram') >= 0) origem = 'instagram';
    else if (fonte.indexOf('facebook') >= 0 || q.get('fbclid') || host.indexOf('facebook') >= 0) origem = 'facebook';
    else if (fonte.indexOf('youtube') >= 0 || host.indexOf('youtube') >= 0 || host.indexOf('youtu.be') >= 0) origem = 'youtube';
    else if (fonte.indexOf('google') >= 0 || host.indexOf('google') >= 0) origem = 'google';
    else if (host || fonte) origem = 'outro';
    return { origem: origem, campanha: q.get('utm_campaign') || '', termo: q.get('utm_term') || '', gclid: q.get('gclid') || '', referencia: host };
  }
  var visita = lerOrigem();
  var nova = true;
  try {
    var guardada = sessionStorage.getItem('ffa_visita');
    if (guardada) { visita = JSON.parse(guardada); nova = false; }
    else sessionStorage.setItem('ffa_visita', JSON.stringify(visita));
  } catch (e) { /* sem armazenamento: vale a página atual */ }

  if (location.pathname.indexOf('/artes') !== 0) enviar('visita', { pagina: location.pathname, origem: visita.origem, nova: nova });

  // Código curto do clique: 5 símbolos e 1 que confere os demais
  function gerarCodigo() {
    var n = new Uint8Array(5);
    (window.crypto || window.msCrypto).getRandomValues(n);
    var codigo = '', soma = 0;
    for (var i = 0; i < 5; i++) { var v = n[i] % 32; soma += v; codigo += ALFABETO[v]; }
    return codigo + ALFABETO[soma % 32];
  }

  // O código em caracteres que não aparecem na tela: o sistema lê e retira
  function oculto(codigo) {
    var t = '';
    for (var i = 0; i < codigo.length; i++) {
      var bits = ALFABETO.indexOf(codigo[i]);
      for (var b = 4; b >= 0; b--) t += String.fromCharCode((bits >> b) & 1 ? 0x200C : 0x200B);
    }
    return t;
  }

  document.addEventListener('click', function (evento) {
    var link = evento.target.closest && evento.target.closest('a[href^="' + NUMERO + '"]');
    if (!link) return;
    var base = link.getAttribute('data-mensagem');
    if (!base) {
      try { base = new URL(link.href).searchParams.get('text') || GERAL; } catch (e) { base = GERAL; }
      link.setAttribute('data-mensagem', base);
    }
    var codigo = gerarCodigo();
    var mensagem = /^Olá/.test(base) ? 'Olá' + oculto(codigo) + base.slice(3) : 'Olá' + oculto(codigo) + '! ' + base;
    link.href = NUMERO + '?text=' + encodeURIComponent(mensagem);
    var marcado = document.querySelector('[data-assunto]');
    enviar('clique', { codigo: codigo, tipo: 'botao', pagina: location.pathname, area: marcado ? marcado.getAttribute('data-assunto') : '',
      origem: visita.origem, campanha: visita.campanha, termo: visita.termo, gclid: visita.gclid, referencia: visita.referencia });
  });
})();
