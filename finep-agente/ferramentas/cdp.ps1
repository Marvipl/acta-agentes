param(
  [Parameter(Mandatory=$true)][string]$Plan   # caminho de um arquivo JSON com a lista de acoes
)
$ErrorActionPreference = "Stop"
$OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# ---- conexao ----
$tabs = (Invoke-WebRequest -Uri "http://127.0.0.1:9222/json/list" -UseBasicParsing -TimeoutSec 10).Content | ConvertFrom-Json
$page = $tabs | Where-Object { $_.type -eq 'page' -and $_.url -like '*finep*' } | Select-Object -First 1
if (-not $page) { Write-Output "ERRO: nenhuma aba do FINEP na porta 9222"; exit 1 }

$ws = New-Object System.Net.WebSockets.ClientWebSocket
$cts = New-Object System.Threading.CancellationTokenSource
$cts.CancelAfter(120000)
$tok = $cts.Token
$ws.ConnectAsync([Uri]$page.webSocketDebuggerUrl, $tok).Wait()

$script:msgId = 0
function Send-Cdp([string]$method, $prms) {
  $script:msgId++
  $myId = $script:msgId
  $obj = @{ id = $myId; method = $method }
  if ($prms) { $obj.params = $prms }
  $json = $obj | ConvertTo-Json -Depth 12 -Compress
  $b = [System.Text.Encoding]::UTF8.GetBytes($json)
  $seg = New-Object System.ArraySegment[byte] -ArgumentList @(,$b)
  $ws.SendAsync($seg, [System.Net.WebSockets.WebSocketMessageType]::Text, $true, $tok).Wait()
  # le mensagens ate achar a resposta com o nosso id (ignora eventos)
  while ($true) {
    $sb = New-Object System.Text.StringBuilder
    $buf = New-Object byte[] 262144
    do {
      $rseg = New-Object System.ArraySegment[byte] -ArgumentList @(,$buf)
      $t = $ws.ReceiveAsync($rseg, $tok); $t.Wait()
      [void]$sb.Append([System.Text.Encoding]::UTF8.GetString($buf, 0, $t.Result.Count))
    } while (-not $t.Result.EndOfMessage)
    $raw = $sb.ToString()
    $r = $raw | ConvertFrom-Json
    if ($r.PSObject.Properties.Name -contains 'id' -and $r.id -eq $myId) { return $r }
  }
}

function Eval([string]$js) {
  $r = Send-Cdp "Runtime.evaluate" @{ expression = $js; returnByValue = $true; awaitPromise = $true }
  if ($r.result.exceptionDetails) {
    return "JS-ERRO: " + $r.result.exceptionDetails.exception.description
  }
  return $r.result.result.value
}

function Click([double]$x, [double]$y) {
  Send-Cdp "Input.dispatchMouseEvent" @{ type="mousePressed"; x=$x; y=$y; button="left"; clickCount=1; buttons=1 } | Out-Null
  Start-Sleep -Milliseconds 40
  Send-Cdp "Input.dispatchMouseEvent" @{ type="mouseReleased"; x=$x; y=$y; button="left"; clickCount=1; buttons=0 } | Out-Null
}

function DblClick([double]$x, [double]$y) {
  Send-Cdp "Input.dispatchMouseEvent" @{ type="mousePressed"; x=$x; y=$y; button="left"; clickCount=1; buttons=1 } | Out-Null
  Send-Cdp "Input.dispatchMouseEvent" @{ type="mouseReleased"; x=$x; y=$y; button="left"; clickCount=1; buttons=0 } | Out-Null
  Start-Sleep -Milliseconds 60
  Send-Cdp "Input.dispatchMouseEvent" @{ type="mousePressed"; x=$x; y=$y; button="left"; clickCount=2; buttons=1 } | Out-Null
  Send-Cdp "Input.dispatchMouseEvent" @{ type="mouseReleased"; x=$x; y=$y; button="left"; clickCount=2; buttons=0 } | Out-Null
}

function KeyPress([string]$key) {
  $map = @{
    "Tab"    = @{ code="Tab";    keyCode=9;  text="" }
    "Enter"  = @{ code="Enter";  keyCode=13; text="`r" }
    "Escape" = @{ code="Escape"; keyCode=27; text="" }
    "Down"   = @{ code="ArrowDown"; keyCode=40; text="" }
    "Up"     = @{ code="ArrowUp";   keyCode=38; text="" }
    "Home"   = @{ code="Home";   keyCode=36; text="" }
  }
  $k = $map[$key]
  if (-not $k) { throw "tecla nao mapeada: $key" }
  $p = @{ type="keyDown"; key=$key; code=$k.code; windowsVirtualKeyCode=$k.keyCode; nativeVirtualKeyCode=$k.keyCode }
  if ($k.text) { $p.text = $k.text }
  Send-Cdp "Input.dispatchKeyEvent" $p | Out-Null
  Send-Cdp "Input.dispatchKeyEvent" @{ type="keyUp"; key=$key; code=$k.code; windowsVirtualKeyCode=$k.keyCode; nativeVirtualKeyCode=$k.keyCode } | Out-Null
}

function SelectAllDelete() {
  # ctrl+a
  Send-Cdp "Input.dispatchKeyEvent" @{ type="keyDown"; key="a"; code="KeyA"; windowsVirtualKeyCode=65; nativeVirtualKeyCode=65; modifiers=2 } | Out-Null
  Send-Cdp "Input.dispatchKeyEvent" @{ type="keyUp";   key="a"; code="KeyA"; windowsVirtualKeyCode=65; nativeVirtualKeyCode=65; modifiers=2 } | Out-Null
  Start-Sleep -Milliseconds 30
  Send-Cdp "Input.dispatchKeyEvent" @{ type="keyDown"; key="Delete"; code="Delete"; windowsVirtualKeyCode=46; nativeVirtualKeyCode=46 } | Out-Null
  Send-Cdp "Input.dispatchKeyEvent" @{ type="keyUp";   key="Delete"; code="Delete"; windowsVirtualKeyCode=46; nativeVirtualKeyCode=46 } | Out-Null
}

Send-Cdp "Runtime.enable" @{} | Out-Null
Send-Cdp "DOM.enable" @{} | Out-Null

# ---- execucao do plano ----
$actions = Get-Content $Plan -Raw -Encoding UTF8 | ConvertFrom-Json
$n = 0
foreach ($a in $actions) {
  $n++
  switch ($a.op) {
    "eval" {
      $v = Eval $a.js
      Write-Output "[$n eval] $v"
    }
    # le o JS de um arquivo: evita o inferno de escape dentro do JSON
    "evalfile" {
      $js = Get-Content $a.file -Raw -Encoding UTF8
      $v = Eval $js
      if ($a.out) { [System.IO.File]::WriteAllText($a.out, [string]$v, [System.Text.Encoding]::UTF8); Write-Output "[$n evalfile] -> $($a.out) ($(([string]$v).Length) chars)" }
      else { Write-Output "[$n evalfile] $v" }
    }
    # digita um texto longo lido de arquivo (campos de 2000+ caracteres)
    "typefile" {
      $txt = Get-Content $a.file -Raw -Encoding UTF8
      $txt = $txt -replace "`r`n", "`n"
      $txt = $txt.TrimEnd("`n")
      Send-Cdp "Input.insertText" @{ text = $txt } | Out-Null
      Write-Output "[$n typefile] $($txt.Length) chars de $($a.file)"
    }
    "click" {
      Click ([double]$a.x) ([double]$a.y)
      Write-Output "[$n click] ($($a.x),$($a.y))"
    }
    # clica no centro do elemento apontado pelo seletor.
    # ATENCAO: rolar e medir tem de ser em chamadas separadas. scrollIntoView pode
    # ser animado; medir no mesmo eval devolve coordenada velha e o clique cai fora.
    "clickSel" {
      $sel = $a.sel | ConvertTo-Json
      $ok = Eval "(function(){var e=document.querySelector($sel); if(!e) return 'NAOACHOU'; e.scrollIntoView({block:'center',behavior:'instant'}); return 'ok';})()"
      if ($ok -eq 'NAOACHOU') { Write-Output "[$n clickSel] NAOACHOU $($a.sel)"; break }
      Start-Sleep -Milliseconds 350
      # Procura um ponto DENTRO do alvo que nao esteja coberto por outro elemento.
      # O formulario tem balões de ajuda (.z-popup-content) que cobrem o centro dos
      # campos; clicar no centro cego acerta o balão e o campo nunca recebe foco.
      $box = Eval @"
(function(){
  var e=document.querySelector($sel);
  if(!e) return 'NAOACHOU';
  var r=e.getBoundingClientRect();
  if(r.width===0&&r.height===0) return 'INVISIVEL';
  var vw=window.innerWidth, vh=window.innerHeight;
  function bom(x,y){
    if(x<2||y<2||x>vw-2||y>vh-2) return false;
    var t=document.elementFromPoint(x,y);
    while(t){ if(t===e) return true; t=t.parentElement; }
    return false;
  }
  var xs=[r.left+Math.min(12,r.width/2), r.left+r.width/2, r.right-Math.min(12,r.width/2)];
  var ys=[r.top+Math.min(10,r.height/2), r.top+r.height/2, r.bottom-Math.min(10,r.height/2)];
  for(var j=0;j<ys.length;j++) for(var i=0;i<xs.length;i++){
    var x=Math.round(xs[i]), y=Math.round(ys[j]);
    if(bom(x,y)) return JSON.stringify({x:x,y:y,ok:1});
  }
  return JSON.stringify({x:Math.round(r.left+r.width/2), y:Math.round(r.top+r.height/2), ok:0});
})()
"@
      if ($box -eq 'NAOACHOU') { Write-Output "[$n clickSel] NAOACHOU (2a medida) $($a.sel)"; break }
      if ($box -eq 'INVISIVEL') { Write-Output "[$n clickSel] elemento invisivel $($a.sel)"; break }
      $b = $box | ConvertFrom-Json
      Click $b.x $b.y
      $aviso = if ($b.ok -eq 0) { " (COBERTO - nenhum ponto livre)" } else { "" }
      Write-Output "[$n clickSel] $($a.sel) em ($($b.x),$($b.y))$aviso"
    }
    # bandbox do ZK (.z-bandpopup): clique simples fecha sem selecionar; precisa de duplo
    "dblclickSel" {
      $box = Eval @"
(function(){
  var e=document.querySelector($($a.sel | ConvertTo-Json));
  if(!e) return 'NAOACHOU';
  e.scrollIntoView({block:'center'});
  var r=e.getBoundingClientRect();
  return JSON.stringify({x:r.left+r.width/2, y:r.top+r.height/2, w:r.width, h:r.height});
})()
"@
      if ($box -eq 'NAOACHOU' -or -not $box) { Write-Output "[$n dblclickSel] NAOACHOU $($a.sel)"; break }
      Start-Sleep -Milliseconds 150
      $b = $box | ConvertFrom-Json
      DblClick $b.x $b.y
      Write-Output "[$n dblclickSel] $($a.sel) em ($([math]::Round($b.x)),$([math]::Round($b.y)))"
    }
    # passa o mouse por cima do elemento: no dhtmlxGantt o botao "+" de cada linha
    # so ganha tamanho quando a linha esta sob o cursor.
    "hoverSel" {
      $sel = $a.sel | ConvertTo-Json
      $box = Eval "(function(){var e=document.querySelector($sel); if(!e) return 'NAOACHOU'; e.scrollIntoView({block:'center',behavior:'instant'}); var r=e.getBoundingClientRect(); if(r.width===0&&r.height===0) return 'INVISIVEL'; return JSON.stringify({x:Math.round(r.left+r.width/2), y:Math.round(r.top+r.height/2)});})()"
      if ($box -eq 'NAOACHOU' -or $box -eq 'INVISIVEL') { Write-Output "[$n hoverSel] $box $($a.sel)"; break }
      $b = $box | ConvertFrom-Json
      Send-Cdp "Input.dispatchMouseEvent" @{ type="mouseMoved"; x=$b.x; y=$b.y; buttons=0 } | Out-Null
      Start-Sleep -Milliseconds 350
      Write-Output "[$n hoverSel] $($a.sel) em ($($b.x),$($b.y))"
    }
    "type" {
      Send-Cdp "Input.insertText" @{ text = $a.text } | Out-Null
      Write-Output "[$n type] $($a.text.Length) chars"
    }
    "clear" {
      SelectAllDelete
      Write-Output "[$n clear]"
    }
    "key" {
      KeyPress $a.key
      Write-Output "[$n key] $($a.key)"
    }
    "wait" {
      Start-Sleep -Milliseconds ([int]$a.ms)
      Write-Output "[$n wait] $($a.ms)ms"
    }
    # espera a fila de requisicoes do ZK esvaziar (estado assentado no servidor)
    "zkidle" {
      $limite = if ($a.ms) { [int]$a.ms } else { 15000 }
      $t0 = Get-Date
      while ($true) {
        # zAu.processing() sozinho nao basta: a troca de passo mostra um overlay
        # "Processando..." enquanto a pagina inteira e' re-renderizada.
        $busy = Eval "(function(){try{ if(window.zAu && zAu.processing && zAu.processing()) return 1; }catch(e){} var b=document.body?document.body.innerText:''; if(b.indexOf('Processando')>=0 && b.length<400) return 1; return 0;})()"
        if ("$busy" -eq "0") { break }
        if (((Get-Date) - $t0).TotalMilliseconds -gt $limite) { Write-Output "[$n zkidle] TIMEOUT"; break }
        Start-Sleep -Milliseconds 200
      }
      Start-Sleep -Milliseconds 300
      Write-Output "[$n zkidle] ok"
    }
    "screenshot" {
      $r = Send-Cdp "Page.captureScreenshot" @{ format="png" }
      [System.IO.File]::WriteAllBytes($a.file, [System.Convert]::FromBase64String($r.result.data))
      Write-Output "[$n screenshot] $($a.file)"
    }
    default { Write-Output "[$n] op desconhecida: $($a.op)" }
  }
}
$ws.CloseAsync([System.Net.WebSockets.WebSocketCloseStatus]::NormalClosure, "", $tok).Wait()
