# Ω GREEK OPTIMIZER — Windows Performance Tool

> *"Purifica. Otimiza. Protege."*  
> **Σ Λ Δ Φ Ψ Π Θ Ξ Γ Β Α**

Script Python unificado para otimização completa do Windows. Combina **Game Mode**, **limpeza de arquivos**, **desinstalação profunda** e **limpeza de mídia e downloads** em um único terminal estilizado — com identidade visual inspirada no estilo Linux/Neofetch, com arte ASCII de Jesus na cruz.

---

## 📋 Requisitos

| Item | Detalhe |
|---|---|
| Sistema Operacional | **Windows 10 / 11** |
| Python | **3.8 ou superior** |
| Privilégios | **Administrador** (recomendado para acesso total) |
| Dependências externas | **Nenhuma** — apenas biblioteca padrão do Python |

---

## 🚀 Como Executar

### ✅ Método recomendado — PowerShell como Administrador

1. Pressione `Win + S` → busque **PowerShell**
2. Clique com o **botão direito** → **"Executar como administrador"**
3. Navegue até a pasta do script:
   ```powershell
   cd C:\Otimizador
   ```
4. Execute:
   ```powershell
   python pc_optimizer.py
   ```

### ⚡ Atalho rápido (duplo clique)

Clique com o botão direito em `pc_optimizer.py` → **"Executar como administrador"**  
*(Se aparecer "Executar com Python", escolha essa opção com botão direito → Propriedades → Abrir com Python)*

### ⚠️ Sem privilégios de Administrador

O script funciona normalmente, porém as seguintes funções serão **puladas automaticamente**:
- Flush de DNS
- Ativação do plano de energia Alto Desempenho
- Limpeza do cache do Windows Update
- Limpeza do Prefetch
- Remoção de chaves de registro residuais

---

## 🖥️ Tela de Abertura (Estilo Neofetch)

Ao iniciar, o terminal exibe automaticamente:

```
  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    Ω  G R E E K   O P T I M I Z E R  Σ
       Λ · Δ · Φ · Ψ · Π · Θ · Ξ · Γ · Β · Α
  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

        ╻               user@DESKTOP-XYZ
  ━━━━━━╋━━━━━━         ─────────────────────────
        ┃               OS    : Windows 11
      ╭─●─╮             Host  : DESKTOP-XYZ
     ─/─┃─\─            Up    : 2h 34m
     /  ┃  \            Shell : Python 3.12.0
    /   ┃   \           CPU   : Intel Core i7-9750H
       ─┃─              RAM   : 5.8 GB livre / 16.0 GB total
        ┃               Disco : C:\ 48.3 GB livre / 476.9 GB
        ┃               Admin : ✓ Administrador
       ╱┃╲
      ╱ ┃ ╲             ███████████████████████████
    ══════════
    ✝  DEUS É FIEL  ✝
```

Ao sair com `[0]`, aparece a **cruz vazia** em dourado representa a ressurreição.

---

## 🗂️ Menu Principal

```
  Ω Opção:

    [1]  🎮  Game Mode          — DNS, plano de energia, processos pesados
    [2]  🗑️  Limpeza            — Temp, Lixeira, Windows Update, Prefetch
    [3]  📦  Deep Uninstaller   — Desinstalar apps e apagar resquícios
    [4]  📁  Mídia & Downloads  — Fotos, vídeos e arquivos antigos
    [5]  🚀  Otimização Total   — Executa todas as opções em sequência
    [0]  ❌  Sair
```

---

## 🎮 Opção 1 — Game Mode

Prepara o PC para máxima performance antes de jogar:

| Função | O que faz | Requer Admin |
|---|---|---|
| **Flush DNS** | `ipconfig /flushdns` — reduz latência/ping | Sim |
| **Alto Desempenho** | Ativa plano de energia via `powercfg` | Sim |
| **Matar Processos** | Detecta e encerra apps pesados com confirmação | Não |

**Processos monitorados:**

| Categoria | Exemplos |
|---|---|
| Navegadores | Chrome, Edge, Opera, Brave |
| Comunicação | Discord, Skype, Slack, Teams, Zoom |
| Outros | Spotify, OneDrive, Outlook |

> Nenhum processo é fechado sem sua confirmação individual.

---

## 🗑️ Opção 2 — Limpeza de Arquivos Inúteis

| Categoria | O que faz | Requer Admin |
|---|---|---|
| **%TEMP% do Sistema** | Apaga pasta temporária do Windows | Não |
| **Lixeira** | Esvazia via API nativa `SHEmptyRecycleBinW` | Não |
| **Cache do Windows Update** | Para serviço `wuauserv`, limpa downloads, reinicia | Sim |
| **Prefetch do Windows** | Remove arquivos `.pf` (recriados automaticamente) | Sim |

Ao final exibe uma **tabela de resumo** com itens removidos e MB liberados por categoria.

> Arquivos em uso pelo sistema são ignorados silenciosamente — o script nunca quebra.

---

## 📦 Opção 3 — Deep Uninstaller

Desinstalação completa em **2 etapas**:

### Etapa 1 — Desinstalação Oficial
- Lê o registro do Windows (`HKLM` + `HKCU`) para obter o desinstalador real
- Injeta flags silenciosas automaticamente:
  - **MsiExec** → `/quiet /norestart`
  - **NSIS** → `/S`

### Etapa 2 — Remoção de Resquícios
Varre ativamente após a desinstalação:

**Pastas residuais em:**
```
%AppData%\Roaming
%AppData%\Local
%AppData%\Local\Programs
%ProgramData%
C:\Program Files
C:\Program Files (x86)
```

**Chaves de registro em:**
```
HKCU\SOFTWARE
HKLM\SOFTWARE
HKLM\SOFTWARE\WOW6432Node
```

### Navegação na lista de apps
```
[número]  Selecionar app para desinstalar
[p]       Próxima página
[v]       Página anterior
[0]       Voltar ao menu principal
```

---

## 📁 Opção 4 — Mídia & Downloads *(novo)*

Limpa arquivos de mídia, downloads antigos e arquivos grandes acumulados:

| Sub-opção | O que faz |
|---|---|
| **[1] Downloads Antigos** | Lista e apaga arquivos com mais de X dias na pasta Downloads |
| **[2] Fotos** | Detecta imagens em Downloads e Pictures para remoção |
| **[3] Vídeos Grandes** | Lista vídeos acima de X MB em Downloads, Videos e Desktop |
| **[4] Limpar Tudo** | Executa as 3 opções acima em sequência |

**Extensões detectadas automaticamente:**

| Tipo | Extensões |
|---|---|
| Fotos | `.jpg` `.jpeg` `.png` `.gif` `.bmp` `.webp` `.heic` `.raw` `.tiff` |
| Vídeos | `.mp4` `.mkv` `.avi` `.mov` `.wmv` `.flv` `.webm` `.m4v` `.3gp` |
| Documentos | `.zip` `.rar` `.7z` `.iso` `.msi` `.exe` `.pdf` `.docx` `.xlsx` |

---

## 🚀 Opção 5 — Otimização Total

Executa em sequência todas as opções:
1. 🎮 Game Mode
2. 🗑️ Limpeza de arquivos inúteis
3. 📁 Mídia & Downloads
4. 📦 Deep Uninstaller

Ideal para uma **manutenção completa** do sistema de uma só vez.

---

## 🔐 Segurança

| Risco | Como é tratado |
|---|---|
| Fechar processo errado | Confirmação S/N individual para cada processo |
| Apagar arquivo importante | Confirmação por categoria antes de qualquer exclusão |
| Arquivos em uso quebrarem o script | `try/except` silencioso em toda operação de I/O |
| Desinstalador travar | Timeout de 180s — processo é encerrado automaticamente |
| Apagar resquícios sem querer | Confirmação separada para pastas e chaves de registro |
| Execução sem admin | Aviso exibido; funções limitadas degradam graciosamente |

---

## 🛠️ Estrutura do Código

```
pc_optimizer.py
│
├── Sistema Visual
│   ├── class C                  Constantes ANSI de cor
│   ├── show_startup()           Tela Neofetch (Jesus na Cruz)
│   ├── show_exit_screen()       Tela de encerramento (Cruz Vazia)
│   └── print_header()           Cabeçalho padrão GREEK OPTIMIZER
│
├── Info do Sistema
│   ├── _get_windows_version()   Versão do Windows
│   ├── _get_cpu_name()          Nome do processador via registro
│   ├── _get_ram_info()          RAM disponível/total via WinAPI
│   ├── _get_disk_info()         Espaço em disco C:\
│   └── _get_uptime()            Tempo ligado via GetTickCount64
│
├── Utilitários Gerais
│   ├── is_admin()               Verifica privilégios de Admin
│   ├── confirm()                Solicita [s/N] colorido
│   ├── run_command()            Executa comandos com timeout
│   └── clean_folder()           Exclusão recursiva segura
│
├── Módulo 1 — Game Mode
│   ├── flush_dns()
│   ├── set_high_performance()
│   └── kill_heavy_processes()
│
├── Módulo 2 — Junk Cleaner
│   ├── _clean_recycle_bin()
│   ├── _clean_windows_update()
│   ├── _clean_prefetch()
│   └── run_junk_cleaner()
│
├── Módulo 3 — Deep Uninstaller
│   ├── _get_installed_apps()
│   ├── _run_uninstaller()
│   ├── _find_leftover_folders()
│   ├── _find_leftover_registry()
│   ├── _deep_clean_app()
│   └── run_deep_uninstaller()
│
├── Módulo 4 — Mídia & Downloads  ← NOVO
│   ├── _scan_files()
│   ├── _print_file_table()
│   ├── _clean_old_downloads()
│   ├── _clean_photos()
│   ├── _clean_videos()
│   └── run_media_cleaner()
│
└── Menu Principal
    └── main_menu()              Loop com opções 1–5 + saída
```

---

## ⚙️ Personalização

Edite estas constantes no início do script:

| Constante | Padrão | Descrição |
|---|---|---|
| `HEAVY_PROCESSES` | lista de `.exe` | Processos encerrados no Game Mode |
| `LEFTOVER_DIRS` | lista de `Path` | Pastas varridas na busca por resquícios |
| `PHOTO_EXT` | set de extensões | Tipos de imagem detectados |
| `VIDEO_EXT` | set de extensões | Tipos de vídeo detectados |
| `MEDIA_DIRS` | dict de `Path` | Pastas varridas no módulo de mídia |

---

## ❓ Perguntas Frequentes

**O script apaga meus arquivos pessoais?**  
Não. Apenas pastas de sistema e arquivos que você confirmar explicitamente.

**O que acontece se o desinstalador abrir uma janela gráfica?**  
Para a maioria dos apps, flags silenciosas são injetadas automaticamente. Alguns desinstaladores antigos abrem mesmo assim — basta concluir pela interface deles. O script aguarda até 180 segundos.

**Preciso reiniciar o PC depois?**  
Não é obrigatório, mas recomendado após desinstalar apps ou limpar o Prefetch.

**O script funciona sem internet?**  
Sim. Todas as operações são 100% locais. Nenhuma conexão de rede é feita.

**Por que o nome GREEK OPTIMIZER?**  
As letras gregas (Ω, Σ, Λ, Δ, Φ...) simbolizam poder, perfeição e tecnologia clássica — identidade visual única para um otimizador de alta performance.

---

## 📄 Licença

Uso pessoal livre. Sem garantias. Use por sua conta e risco.

---

*Ω  GREEK OPTIMIZER  Σ — Que Deus abençoe sua máquina!  ✝*
