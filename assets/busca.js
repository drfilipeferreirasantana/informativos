// Pesquisa dos informativos (pedido do Dr. Filipe, 14/11/2026).
// Lê busca.json (gerado por ferramentas/gerar.py) e mostra os informativos que combinam com o que a pessoa digitou.
// Ignora acentos e maiúsculas, aceita plural e alguns sinônimos do jeito que as pessoas falam.
(function () {
  var campo = document.getElementById('busca');
  if (!campo) return;
  var info = document.getElementById('busca-info');
  var res = document.getElementById('resultados');
  var normal = document.getElementById('vitrine-normal');
  var dados = null, pedindo = null, espera = null;
  var linkWhats = document.querySelector('.nav-whats');
  var whats = linkWhats ? linkWhats.getAttribute('href') : '#';

  var SINONIMOS = {
    pensao: ['alimentos', 'alimenticia'], alimentos: ['pensao'],
    divorcio: ['separacao', 'partilha'], separacao: ['divorcio'],
    heranca: ['inventario', 'sucessao', 'testamento'], inventario: ['heranca'],
    demissao: ['rescisao', 'dispensa', 'demitido'], demitido: ['demissao', 'dispensa', 'rescisao'],
    rescisao: ['demissao', 'dispensa', 'verbas'], acerto: ['rescisao', 'verbas'],
    inss: ['aposentadoria', 'beneficio', 'auxilio', 'previdenciario'], aposentadoria: ['inss'],
    beneficio: ['inss', 'auxilio'], guarda: ['filho', 'convivencia'], visita: ['convivencia', 'guarda'],
    nome: ['negativado', 'serasa'], serasa: ['negativado', 'nome'], banco: ['juros', 'emprestimo'],
    patrao: ['empresa', 'empregador'], empresa: ['empregador'], uniao: ['companheiro', 'convivencia'],
    agua: ['samarco', 'rio'], samarco: ['rio', 'agua'], acidente: ['acidentado']
  };
  var IGNORAR = {de: 1, da: 1, do: 1, das: 1, dos: 1, e: 1, o: 1, a: 1, os: 1, as: 1, em: 1, no: 1, na: 1,
    um: 1, uma: 1, para: 1, por: 1, com: 1, que: 1, se: 1, meu: 1, minha: 1, eu: 1, ao: 1, como: 1, qual: 1, tem: 1,
    fui: 1, sou: 1, estou: 1, foi: 1, fiquei: 1, quero: 1, preciso: 1, posso: 1, pode: 1, sobre: 1, mais: 1, ja: 1,
    nao: 1, sim: 1, quando: 1, quanto: 1, onde: 1, porque: 1, isso: 1, esse: 1, essa: 1, ele: 1, ela: 1, me: 1, mim: 1, esta: 1, estao: 1, ta: 1, tenho: 1, ter: 1, tinha: 1, saber: 1, fazer: 1, faco: 1};

  function sem(t) {
    return (t || '').normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase();
  }
  function campo_(t) { // texto sem acento, só letras e números, com espaço antes de cada palavra
    return ' ' + sem(t).replace(/[^a-z0-9%]+/g, ' ');
  }
  function raiz(p) { // palavra longa vira o começo dela ("divorciar" acha "divórcio"); "pensoes" acha "pensao"
    if (p.length >= 7) return p.slice(0, 5);
    if (p.length > 4 && /oes$/.test(p)) return p.slice(0, -3);
    if (p.length > 4 && /aes$/.test(p)) return p.slice(0, -3);
    if (p.length > 4 && /s$/.test(p)) return p.slice(0, -1);
    return p;
  }
  function esc(t) {
    return t.replace(/[&<>"]/g, function (c) { return {'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;'}[c]; });
  }
  function carregar() {
    if (!pedindo) {
      pedindo = fetch('busca.json?v=' + (document.lastModified || '')).then(function (r) { return r.json(); })
        .then(function (lista) {
          dados = lista.map(function (x) {
            return {x: x, t: campo_(x.t), d: campo_(x.d), k: campo_(x.k)};
          });
        });
    }
    return pedindo;
  }
  function pontos(item, termos, todas) {
    var total = 0, achou = 0;
    for (var i = 0; i < termos.length; i++) {
      var melhor = 0;
      termos[i].forEach(function (v, j) {
        var peso = j === 0 ? 1 : 0.6; // a palavra digitada vale mais que o sinônimo
        var p = 0;
        v = ' ' + v; // começo de palavra: "rio" não acha "período"
        if (item.t.indexOf(v) > -1) p = 6; else if (item.d.indexOf(v) > -1) p = 3; else if (item.k.indexOf(v) > -1) p = 1;
        melhor = Math.max(melhor, p * peso);
      });
      if (!melhor && todas) return 0; // primeiro, todas as palavras precisam aparecer (ou um sinônimo delas)
      if (melhor) achou++;
      total += melhor;
    }
    if (!achou) return 0;
    return total + achou * 4 + item.x.o; // guias e calculadora sobem um pouco
  }
  function cartao(x) {
    return '<a class="cartao" href="' + esc(x.u) + '"><img src="' + esc(x.i) + '" width="480" height="300" loading="lazy" alt="">' +
      '<span class="meta">' + esc(x.a) + '</span><h2>' + esc(x.t) + '</h2>' +
      '<span class="resposta-curta">' + esc(x.d) + '</span></a>';
  }
  function mostrar(texto) {
    var q = sem(texto).replace(/[^a-z0-9% ]/g, ' ').trim();
    var palavras = q.split(/\s+/).filter(function (p) { return p.length > 1 && !IGNORAR[p]; });
    if (!palavras.length) {
      res.hidden = true; info.hidden = true; normal.hidden = false; res.innerHTML = '';
      return;
    }
    carregar().then(function () {
      var termos = palavras.map(function (p) {
        var r = raiz(p);
        return [r].concat(SINONIMOS[p] || SINONIMOS[r] || []);
      });
      function buscar(todas) {
        return dados.map(function (it) { return {it: it, p: pontos(it, termos, todas)}; })
          .filter(function (a) { return a.p > 0; })
          .sort(function (a, b) { return b.p - a.p; });
      }
      var achados = buscar(true), parcial = false;
      if (!achados.length && termos.length > 1) { achados = buscar(false); parcial = true; }
      normal.hidden = true;
      info.hidden = false;
      if (!achados.length) {
        res.hidden = true;
        info.innerHTML = 'Nenhum informativo encontrado para <b>' + esc(texto.trim()) + '</b>. Tente outra palavra, ' +
          'ou mande a sua dúvida pelo <a href="' + esc(whats) + '" target="_blank" rel="noopener">WhatsApp</a>.';
        return;
      }
      info.innerHTML = (parcial ? 'Nada com todas as palavras de <b>' + esc(texto.trim()) + '</b>. Os mais próximos:' :
        achados.length + (achados.length > 1 ? ' informativos encontrados' : ' informativo encontrado') +
        ' para <b>' + esc(texto.trim()) + '</b>') + ' <button type="button" class="busca-limpar">Limpar pesquisa</button>';
      res.innerHTML = achados.slice(0, 30).map(function (a) { return cartao(a.it.x); }).join('');
      res.hidden = false;
    }).catch(function () {
      info.hidden = false;
      info.textContent = 'Não foi possível carregar a pesquisa agora. Tente de novo em instantes.';
    });
  }
  function guardar(texto) { // endereço com ?q= permite voltar à pesquisa e compartilhá-la
    var u = new URL(location.href);
    if (texto.trim()) u.searchParams.set('q', texto.trim()); else u.searchParams.delete('q');
    history.replaceState(null, '', u.pathname + u.search + u.hash);
  }

  campo.addEventListener('focus', carregar);
  campo.addEventListener('input', function () {
    clearTimeout(espera);
    espera = setTimeout(function () { mostrar(campo.value); guardar(campo.value); }, 180);
  });
  info.addEventListener('click', function (ev) {
    if (ev.target.classList.contains('busca-limpar')) { campo.value = ''; mostrar(''); guardar(''); campo.focus(); }
  });

  var inicial = new URLSearchParams(location.search).get('q');
  if (inicial) { campo.value = inicial; mostrar(inicial); }
  else if (location.hash === '#pesquisa') campo.focus();
  window.addEventListener('hashchange', function () { if (location.hash === '#pesquisa') campo.focus(); });
})();
