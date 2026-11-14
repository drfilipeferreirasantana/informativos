/* Calculadora de rescisão (CLT), valores brutos estimados.
   Regras: CLT arts. 146, 147, 477, 479, 484-A e 487; Lei 4.090/1962 (13º);
   Lei 12.506/2011 (aviso proporcional); Lei 8.036/1990, art. 18 (multa do FGTS);
   TST, Súmulas 171 e 261 e OJ 82 da SDI-1 (projeção do aviso). */
(function () {
  'use strict';
  var DIA = 864e5;

  function data(v) { var p = (v || '').split('-'); return p.length === 3 ? new Date(+p[0], +p[1] - 1, +p[2]) : null; }
  function addDias(d, n) { return new Date(d.getFullYear(), d.getMonth(), d.getDate() + n); }
  function anosCompletos(ini, fim) {
    var a = fim.getFullYear() - ini.getFullYear();
    if (fim.getMonth() < ini.getMonth() || (fim.getMonth() === ini.getMonth() && fim.getDate() < ini.getDate())) a--;
    return Math.max(0, a);
  }
  function aniversario(ini, ano) { return new Date(ano, ini.getMonth(), ini.getDate()); }
  // meses de 15 dias ou mais entre duas datas, contados a partir de "ini" (para férias proporcionais)
  function avosDesde(ini, fim) {
    var n = 0, cur = new Date(ini);
    while (true) {
      var prox = new Date(cur.getFullYear(), cur.getMonth() + 1, cur.getDate());
      if (prox <= addDias(fim, 1)) { n++; cur = prox; } else break;
    }
    var resto = Math.round((addDias(fim, 1) - cur) / DIA);
    if (resto >= 15) n++;
    return Math.min(n, 12);
  }
  // meses do ano civil com 15 dias ou mais trabalhados (para o 13º)
  function avos13(adm, fim) {
    var n = 0, ano = fim.getFullYear();
    for (var m = 0; m <= fim.getMonth(); m++) {
      var i = new Date(ano, m, 1), f = new Date(ano, m + 1, 0);
      if (adm > i) i = adm;
      if (fim < f) f = fim;
      var dias = Math.round((f - i) / DIA) + 1;
      if (dias >= 15) n++;
    }
    return n;
  }
  function brl(v) { return v.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' }); }
  function num(v) { return parseFloat(String(v || '').replace(/\./g, '').replace(',', '.')) || 0; }

  var f = document.getElementById('calc');
  if (!f) return;
  var saida = document.getElementById('resultado');
  var tipo = f.elements.tipo, aviso = document.getElementById('linha-aviso');

  function ajustarAviso() {
    var t = tipo.value;
    aviso.hidden = !(t === 'sem_justa' || t === 'pedido' || t === 'acordo');
    var op = f.elements.aviso.options;
    op[0].text = t === 'pedido' ? 'Cumpri o aviso (trabalhei os 30 dias)' : 'Trabalhado';
    op[1].text = t === 'pedido' ? 'Não cumpri o aviso' : 'Indenizado (pago sem trabalhar)';
  }
  tipo.addEventListener('change', ajustarAviso);
  ajustarAviso();

  f.addEventListener('submit', function (ev) {
    ev.preventDefault();
    var sal = num(f.elements.salario.value), adm = data(f.elements.admissao.value), fim = data(f.elements.saida.value);
    var t = tipo.value, av = f.elements.aviso.value, vencidas = parseInt(f.elements.vencidas.value, 10) || 0;
    var fgtsInf = num(f.elements.fgts.value);
    if (!sal || !adm || !fim || fim < adm) {
      saida.innerHTML = '<p class="calc-erro">Confira o salário e as datas de entrada e de saída.</p>';
      saida.hidden = false; return;
    }
    var linhas = [], total = 0, desconto = 0;
    function item(nome, valor, base, nota) { linhas.push([nome, valor, base, nota || '']); total += valor; }

    var anos = anosCompletos(adm, fim);
    var diasAviso = Math.min(30 + 3 * anos, 90);
    var indenizado = (t === 'sem_justa' || t === 'acordo') && av === 'indenizado';
    var projetada = indenizado ? addDias(fim, diasAviso) : fim; // o aviso indenizado conta como tempo de serviço

    // saldo de salário
    var diasMes = Math.min(fim.getDate(), 30);
    item('Saldo de salário (' + diasMes + ' dias)', sal / 30 * diasMes, 'CLT, art. 477');

    // aviso prévio
    if (indenizado) {
      var vAviso = sal / 30 * diasAviso;
      if (t === 'acordo') item('Aviso prévio indenizado (metade de ' + diasAviso + ' dias)', vAviso / 2, 'CLT, art. 484-A, I, a');
      else item('Aviso prévio indenizado (' + diasAviso + ' dias)', vAviso, 'CLT, art. 487; Lei 12.506/2011');
    }
    if (t === 'pedido' && av === 'indenizado') { desconto = sal; }

    // 13º proporcional
    if (t !== 'justa') {
      var a13 = avos13(adm, projetada);
      if (a13 > 0) item('13º salário proporcional (' + a13 + '/12)', sal / 12 * a13, 'Lei 4.090/1962');
    }

    // férias vencidas
    if (vencidas > 0) {
      item('Férias vencidas + 1/3 (' + vencidas + (vencidas > 1 ? ' períodos' : ' período') + ')', sal * vencidas * 4 / 3, 'CLT, art. 146; Constituição, art. 7º, XVII',
        vencidas > 1 ? 'Férias não dadas no prazo podem ser devidas em dobro (CLT, art. 137).' : '');
    }
    // férias proporcionais
    if (t !== 'justa') {
      var ultimo = aniversario(adm, projetada.getFullYear());
      if (ultimo > projetada) ultimo = aniversario(adm, projetada.getFullYear() - 1);
      if (ultimo < adm) ultimo = adm;
      var avf = avosDesde(ultimo, projetada);
      if (avf > 0 && avf < 12) item('Férias proporcionais + 1/3 (' + avf + '/12)', sal / 12 * avf * 4 / 3, 'CLT, arts. 146 e 147; Súmulas 171 e 261 do TST');
    }

    // FGTS
    var meses = Math.max(1, Math.round((fim - adm) / DIA / 30.4375));
    var fgts = fgtsInf || sal * 0.08 * meses * (1 + 1 / 12 + 1 / 36); // salários, 13º e 1/3 de férias
    var notaF = fgtsInf ? '' : 'Saldo do FGTS estimado; confira o extrato no aplicativo do FGTS.';
    if (t === 'sem_justa') item('Multa de 40% do FGTS', fgts * 0.4, 'Lei 8.036/1990, art. 18, § 1º', notaF);
    if (t === 'acordo') item('Multa de 20% do FGTS', fgts * 0.2, 'CLT, art. 484-A, I, b', notaF);
    if (t === 'experiencia_antecipada') item('Indenização do art. 479 (metade dos dias que faltavam)', 0, 'CLT, art. 479', 'Informe ao escritório quantos dias faltavam para o fim do contrato.');

    var corpo = linhas.filter(function (l) { return l[1] > 0 || l[3]; }).map(function (l) {
      return '<tr><td>' + l[0] + (l[3] ? '<small>' + l[3] + '</small>' : '') + '<small class="calc-base">' + l[2] + '</small></td><td>' + (l[1] > 0 ? brl(l[1]) : 'a calcular') + '</td></tr>';
    }).join('');
    if (desconto) corpo += '<tr class="calc-desconto"><td>Desconto do aviso não cumprido<small class="calc-base">CLT, art. 487, § 2º</small></td><td>- ' + brl(desconto) + '</td></tr>';

    var saque = { sem_justa: 'Saque de todo o FGTS e direito ao seguro-desemprego, se cumpridos os requisitos.',
      acordo: 'Saque de até 80% do FGTS. Não há seguro-desemprego.',
      pedido: 'Não há saque do FGTS nem seguro-desemprego.',
      justa: 'Não há saque do FGTS nem seguro-desemprego. A justa causa pode ser contestada se a falta não for provada.',
      experiencia: 'No fim do contrato de experiência há saque do FGTS, sem multa de 40% e sem seguro-desemprego.',
      experiencia_antecipada: 'Na dispensa antes do fim da experiência há saque do FGTS e multa de 40%, além da indenização do art. 479.' }[t];

    saida.innerHTML = '<h2>Estimativa da sua rescisão</h2>' +
      '<table class="calc-tabela"><tbody>' + corpo + '</tbody><tfoot><tr><th>Total bruto estimado</th><th>' + brl(total - desconto) + '</th></tr></tfoot></table>' +
      '<p class="calc-nota">' + saque + '</p>' +
      '<p class="calc-nota">Valores brutos, antes dos descontos de INSS e Imposto de Renda. A empresa tem 10 dias, contados do fim do contrato, para pagar; se atrasar, deve multa de um salário (CLT, art. 477, §§ 6º e 8º).</p>' +
      '<p class="calc-aviso">Estimativa informativa. Horas extras, comissões, adicionais e outras verbas mudam o resultado, e cada caso depende dos documentos.</p>';
    saida.hidden = false;
    saida.scrollIntoView({ behavior: 'smooth', block: 'start' });
  });
})();
