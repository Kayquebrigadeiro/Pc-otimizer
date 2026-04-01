"""
╔══════════════════════════════════════════════════════════════╗
║          PC OPTIMIZER — Game Mode + Cleaner + Uninstaller    ║
║          Otimização completa do Windows em um só script      ║
╚══════════════════════════════════════════════════════════════╝

  Requer Python 3.8+ | Administrador recomendado para acesso total.
  Uso: python pc_optimizer.py
"""

import os
import sys
import shutil
import ctypes
import winreg
import tempfile
import subprocess
import time
from pathlib import Path


# ══════════════════════════════════════════════════════════════
# UTILIDADES GERAIS
# ══════════════════════════════════════════════════════════════

def is_admin() -> bool:
    """Verifica se o script roda com privilégios de Administrador."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False


def confirm(prompt: str) -> bool:
    """Solicita confirmação S/N do usuário."""
    answer = input(f"\n  {prompt} [s/N]: ").strip().lower()
    return answer in ("s", "sim", "y", "yes")


def bytes_to_mb(size: int) -> float:
    """Converte bytes para megabytes."""
    return round(size / (1024 * 1024), 2)


def clear_screen():
    os.system("cls")


def print_header(subtitle: str = ""):
    """Exibe o cabeçalho padrão do programa."""
    clear_screen()
    print("═" * 62)
    print("       ⚡  PC OPTIMIZER  —  Windows Performance Tool")
    if subtitle:
        print(f"       {subtitle}")
    print("═" * 62)
    mode = "✅ Administrador" if is_admin() else "⚠️  Usuário comum (acesso limitado)"
    print(f"  Modo: {mode}")
    print("═" * 62)


def run_command(cmd: list, timeout: int = 120) -> tuple:
    """Executa um comando do sistema de forma segura. Retorna (código, saída)."""
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return r.returncode, r.stdout + r.stderr
    except subprocess.TimeoutExpired:
        return -1, "Timeout."
    except Exception as e:
        return -1, str(e)


def clean_folder(folder: Path) -> tuple:
    """
    Apaga recursivamente o conteúdo de uma pasta.
    Arquivos em uso são ignorados silenciosamente.
    Retorna (itens_deletados, bytes_liberados).
    """
    deleted, freed = 0, 0
    if not folder.exists():
        return 0, 0

    for item in folder.iterdir():
        try:
            if item.is_file() or item.is_symlink():
                freed += item.stat().st_size
                item.unlink()
                deleted += 1
            elif item.is_dir():
                freed += sum(f.stat().st_size for f in item.rglob("*") if f.is_file())
                shutil.rmtree(item, ignore_errors=True)
                deleted += 1
        except (PermissionError, OSError):
            pass

    return deleted, freed


# ══════════════════════════════════════════════════════════════
# MÓDULO 1 — GAME MODE (Otimização para Jogos)
# ══════════════════════════════════════════════════════════════

# Processos conhecidos por consumir RAM em segundo plano
HEAVY_PROCESSES = [
    "chrome.exe", "msedge.exe", "opera.exe", "brave.exe",
    "discord.exe", "skype.exe", "slack.exe", "teams.exe",
    "zoom.exe", "spotify.exe", "onedrive.exe", "outlook.exe",
]


def flush_dns():
    """Limpa o cache DNS para reduzir latência/ping. Requer Admin."""
    print("\n  🌐 Limpando cache DNS...")
    if not is_admin():
        print("  ⚠️  Requer Administrador — pulado.")
        return
    code, _ = run_command(["ipconfig", "/flushdns"])
    print("  ✅ Cache DNS limpo." if code == 0 else "  ❌ Falha ao limpar DNS.")


def set_high_performance():
    """Ativa o plano de energia 'Alto Desempenho'. Requer Admin."""
    print("\n  ⚡ Ativando plano de energia 'Alto Desempenho'...")
    if not is_admin():
        print("  ⚠️  Requer Administrador — pulado.")
        return
    # GUID nativo do plano Alto Desempenho do Windows
    GUID = "8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c"
    code, _ = run_command(["powercfg", "/setactive", GUID])
    print("  ✅ Plano ativado." if code == 0 else "  ❌ Falha ao mudar plano de energia.")


def kill_heavy_processes():
    """Detecta processos pesados em execução e encerra os que o usuário confirmar."""
    print("\n  🔫 Verificando processos pesados em execução...")

    # Lê a lista de processos ativos via tasklist
    code, output = run_command(["tasklist", "/fo", "csv", "/nh"])
    if code != 0:
        print("  ❌ Não foi possível listar processos.")
        return

    running = [p for p in HEAVY_PROCESSES if p.lower() in output.lower()]

    if not running:
        print("  ✅ Nenhum processo pesado encontrado.")
        return

    print(f"  Encontrados {len(running)} processo(s):")
    for p in running:
        print(f"    • {p}")

    killed = 0
    for proc in running:
        if confirm(f"Encerrar '{proc}'?"):
            code, _ = run_command(["taskkill", "/f", "/im", proc])
            if code == 0:
                print(f"    ✅ '{proc}' encerrado.")
                killed += 1
            else:
                print(f"    ❌ Não foi possível encerrar '{proc}'.")
        else:
            print(f"    ⏭️  '{proc}' mantido.")

    print(f"\n  📊 {killed}/{len(running)} processos encerrados.")


def run_game_mode():
    """Executa todas as otimizações do Game Mode em sequência."""
    print_header("🎮  GAME MODE — Otimização para Jogos")
    print()
    flush_dns()
    set_high_performance()
    kill_heavy_processes()
    print("\n  ✅ Game Mode concluído! Bons jogos.")
    input("\n  Pressione ENTER para voltar ao menu...")


# ══════════════════════════════════════════════════════════════
# MÓDULO 2 — LIMPEZA DE ARQUIVOS INÚTEIS
# ══════════════════════════════════════════════════════════════

WUPDATE_CACHE = Path(r"C:\Windows\SoftwareDistribution\Download")
PREFETCH_DIR  = Path(r"C:\Windows\Prefetch")


def _clean_recycle_bin() -> tuple:
    """Esvazia a Lixeira usando a API nativa do Windows."""
    freed = 0
    try:
        info = ctypes.create_string_buffer(32)
        ctypes.windll.shell32.SHQueryRecycleBinW(None, info)
        freed = max(0, ctypes.cast(info, ctypes.POINTER(ctypes.c_int64))[1])
    except Exception:
        freed = 0
    ret = ctypes.windll.shell32.SHEmptyRecycleBinW(None, None, 0x0001 | 0x0002)
    return (1, freed) if ret in (0, -2147418113) else (0, 0)


def _clean_windows_update() -> tuple:
    """Limpa o cache de downloads do Windows Update (para serviço antes de apagar)."""
    if not is_admin():
        print("  ⚠️  Requer Administrador — pulado.")
        return 0, 0
    os.system("net stop wuauserv >nul 2>&1")
    result = clean_folder(WUPDATE_CACHE)
    os.system("net start wuauserv >nul 2>&1")
    return result


def _clean_prefetch() -> tuple:
    """Apaga arquivos de pré-carregamento do Windows (recriados automaticamente)."""
    if not is_admin():
        print("  ⚠️  Requer Administrador — pulado.")
        return 0, 0
    return clean_folder(PREFETCH_DIR)


JUNK_CATEGORIES = [
    ("%TEMP% do Sistema",       lambda: clean_folder(Path(tempfile.gettempdir()))),
    ("Lixeira",                 _clean_recycle_bin),
    ("Cache do Windows Update", _clean_windows_update),
    ("Prefetch do Windows",     _clean_prefetch),
]


def run_junk_cleaner():
    """Menu de limpeza: confirma cada categoria antes de apagar."""
    print_header("🗑️  LIMPEZA DE ARQUIVOS INÚTEIS")
    print()

    summary = []
    total_deleted, total_freed = 0, 0

    for name, func in JUNK_CATEGORIES:
        print(f"  ── {name}")
        if not confirm(f"Limpar '{name}'?"):
            print("  ⏭️  Pulado.\n")
            continue

        deleted, freed = func()
        freed_mb = bytes_to_mb(freed)
        total_deleted += deleted
        total_freed   += freed_mb
        summary.append((name, deleted, freed_mb))
        print(f"  ✅ {deleted} item(ns) | {freed_mb} MB liberados\n")

    # Resumo final
    print("\n" + "═" * 58)
    print("  📊 RESUMO DA LIMPEZA")
    print("═" * 58)
    if not summary:
        print("  Nenhuma categoria executada.")
    else:
        W = 28
        print(f"  {'Categoria':<{W}} {'Itens':>6}  {'Liberado':>10}")
        print("  " + "─" * 48)
        for cat, d, f in summary:
            print(f"  {cat:<{W}} {d:>6}  {f:>8.2f} MB")
        print("  " + "─" * 48)
        print(f"  {'TOTAL':<{W}} {total_deleted:>6}  {total_freed:>8.2f} MB")
    print("═" * 58)

    input("\n  Pressione ENTER para voltar ao menu...")


# ══════════════════════════════════════════════════════════════
# MÓDULO 3 — DEEP UNINSTALLER
# ══════════════════════════════════════════════════════════════

# Chaves do registro onde ficam os apps instalados
UNINSTALL_KEYS = [
    (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
    (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"),
    (winreg.HKEY_CURRENT_USER,  r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
]

# Pastas onde apps costumam deixar resquícios
LEFTOVER_DIRS = [
    Path(os.environ.get("APPDATA",      "")),
    Path(os.environ.get("LOCALAPPDATA", "")),
    Path(os.environ.get("LOCALAPPDATA", "")) / "Programs",
    Path(os.environ.get("PROGRAMDATA",  "")),
    Path(r"C:\Program Files"),
    Path(r"C:\Program Files (x86)"),
]

# Raízes do registro para buscar chaves residuais
LEFTOVER_REG_ROOTS = [
    (winreg.HKEY_CURRENT_USER,  r"SOFTWARE"),
    (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE"),
    (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node"),
]


def _get_installed_apps() -> list:
    """
    Lê o registro do Windows e retorna todos os apps instalados.
    Filtra entradas sem nome, sem desinstalador e atualizações de sistema.
    """
    apps = {}

    for hive, key_path in UNINSTALL_KEYS:
        try:
            key = winreg.OpenKey(hive, key_path)
        except OSError:
            continue

        for i in range(winreg.QueryInfoKey(key)[0]):
            try:
                sub_name = winreg.EnumKey(key, i)
                sub_key  = winreg.OpenKey(key, sub_name)

                def _val(field, sk=sub_key):
                    try:
                        return winreg.QueryValueEx(sk, field)[0]
                    except OSError:
                        return ""

                name      = _val("DisplayName").strip()
                uninstall = _val("UninstallString").strip()

                if not name or not uninstall:
                    continue
                if any(s in name for s in ("Update for", "Security Update", "Hotfix", "KB4", "KB5")):
                    continue

                if name not in apps:
                    apps[name] = {
                        "name":             name,
                        "version":          _val("DisplayVersion"),
                        "publisher":        _val("Publisher"),
                        "uninstall_cmd":    uninstall,
                        "install_location": _val("InstallLocation"),
                    }

                winreg.CloseKey(sub_key)
            except OSError:
                continue

        winreg.CloseKey(key)

    return sorted(apps.values(), key=lambda x: x["name"].lower())


def _run_uninstaller(cmd: str) -> bool:
    """
    Executa o desinstalador oficial do app.
    Injeta flags silenciosas para MsiExec e NSIS quando possível.
    """
    cmd_lower = cmd.lower()

    if "msiexec" in cmd_lower:
        cmd = cmd.replace("/I{", "/X{").replace("/i{", "/X{")
        if "/quiet" not in cmd_lower and "/q" not in cmd_lower:
            cmd += " /quiet /norestart"
    elif "uninst" in cmd_lower or "_uninstall" in cmd_lower:
        if "/s" not in cmd_lower:
            cmd += " /S"

    print(f"\n  ▶ Executando desinstalador...")
    print(f"    {cmd[:80]}{'...' if len(cmd) > 80 else ''}")

    try:
        proc = subprocess.Popen(cmd, shell=True)
        proc.wait(timeout=180)
        return proc.returncode in (0, 1605, 1614, 3010)
    except subprocess.TimeoutExpired:
        proc.kill()
        print("  ⚠️  Desinstalador não respondeu — processo encerrado.")
        return False
    except Exception as e:
        print(f"  ❌ Erro: {e}")
        return False


def _find_leftover_folders(app_name: str, install_location: str) -> list:
    """Busca pastas residuais do app em locais comuns do Windows."""
    words    = [w for w in app_name.split() if len(w) > 3]
    keywords = list({app_name.lower()} | {w.lower() for w in words})
    found    = []

    if install_location:
        p = Path(install_location)
        if p.exists():
            found.append(p)

    for base in LEFTOVER_DIRS:
        if not base.exists():
            continue
        try:
            for child in base.iterdir():
                if child.is_dir() and any(kw in child.name.lower() for kw in keywords):
                    if child not in found:
                        found.append(child)
        except (PermissionError, OSError):
            pass

    return found


def _find_leftover_registry(app_name: str) -> list:
    """Busca chaves de registro residuais do app. Retorna lista de (hive, caminho)."""
    words    = [w for w in app_name.split() if len(w) > 3]
    keywords = list({app_name.lower()} | {w.lower() for w in words})
    found    = []

    for hive, base_path in LEFTOVER_REG_ROOTS:
        try:
            base_key = winreg.OpenKey(hive, base_path)
            for i in range(winreg.QueryInfoKey(base_key)[0]):
                try:
                    sub_name = winreg.EnumKey(base_key, i)
                    if any(kw in sub_name.lower() for kw in keywords):
                        found.append((hive, f"{base_path}\\{sub_name}"))
                except OSError:
                    continue
            winreg.CloseKey(base_key)
        except OSError:
            continue

    return found


def _delete_registry_key(hive, key_path: str):
    """Apaga uma chave de registro e todas as subchaves via 'reg delete'."""
    hive_name = "HKLM" if hive == winreg.HKEY_LOCAL_MACHINE else "HKCU"
    run_command(["reg", "delete", f"{hive_name}\\{key_path}", "/f"])


def _deep_clean_app(app: dict):
    """
    Etapa 2 da desinstalação: remove TODOS os resquícios.
    Varre pastas comuns e chaves de registro, pedindo confirmação.
    """
    name             = app["name"]
    install_location = app.get("install_location", "")

    print(f"\n  🔍 Procurando resquícios de '{name}'...")
    time.sleep(1)  # Aguarda o desinstalador liberar arquivos

    # ── Pastas residuais ─────────────────────────────────────
    folders = _find_leftover_folders(name, install_location)

    if folders:
        print(f"\n  📂 {len(folders)} pasta(s) residual(is) encontrada(s):")
        for p in folders:
            try:
                size_mb = bytes_to_mb(sum(f.stat().st_size for f in p.rglob("*") if f.is_file()))
            except Exception:
                size_mb = 0.0
            print(f"    • {p}  ({size_mb} MB)")

        if confirm("  Apagar todas as pastas residuais?"):
            for p in folders:
                try:
                    shutil.rmtree(p, ignore_errors=True)
                    print(f"    🗑️  Removido: {p.name}")
                except Exception as e:
                    print(f"    ⚠️  Erro ao remover '{p.name}': {e}")
    else:
        print("  ✅ Nenhuma pasta residual encontrada.")

    # ── Chaves de registro ───────────────────────────────────
    if is_admin():
        reg_keys = _find_leftover_registry(name)

        if reg_keys:
            print(f"\n  🗝️  {len(reg_keys)} chave(s) de registro encontrada(s):")
            for _, path in reg_keys:
                print(f"    • {path}")

            if confirm("  Apagar essas chaves do registro?"):
                for hive, path in reg_keys:
                    _delete_registry_key(hive, path)
                    print(f"    🗑️  Removido: ...\\{path.split(chr(92))[-1]}")
        else:
            print("  ✅ Nenhuma chave de registro residual encontrada.")
    else:
        print("\n  ⚠️  Limpeza de registro ignorada (requer Administrador).")


def _handle_uninstall(app: dict):
    """Conduz o fluxo completo: confirmar → desinstalar → limpar resquícios."""
    print_header("📦  DEEP UNINSTALLER")
    print(f"\n  App selecionado:\n")
    print(f"    Nome:       {app['name']}")
    print(f"    Versão:     {app['version'] or '—'}")
    print(f"    Fabricante: {app['publisher'] or '—'}")
    if app["install_location"]:
        print(f"    Local:      {app['install_location']}")
    print()

    if not confirm(f"Desinstalar '{app['name']}' completamente?"):
        print("  ⏭️  Cancelado.")
        time.sleep(1)
        return

    print("\n  ── ETAPA 1: Desinstalação oficial ──")
    success = _run_uninstaller(app["uninstall_cmd"])
    print("  ✅ Desinstalador concluído." if success else
          "  ⚠️  Desinstalador retornou erro. Prosseguindo com limpeza...")

    print("\n  ── ETAPA 2: Remoção de Resquícios ──")
    _deep_clean_app(app)

    print(f"\n  ✅ '{app['name']}' removido completamente!")
    input("\n  Pressione ENTER para voltar à lista...")


def run_deep_uninstaller():
    """Exibe lista paginada de apps instalados e permite selecionar para desinstalar."""
    print_header("📦  DEEP UNINSTALLER")
    print("\n  Carregando aplicativos instalados...\n")

    apps = _get_installed_apps()
    if not apps:
        print("  ❌ Nenhum aplicativo encontrado no registro.")
        input("\n  ENTER para voltar...")
        return

    PAGE        = 20
    page        = 0
    total_pages = (len(apps) - 1) // PAGE + 1

    while True:
        print_header("📦  DEEP UNINSTALLER")
        start = page * PAGE
        end   = min(start + PAGE, len(apps))

        print(f"\n  Apps instalados — Página {page + 1}/{total_pages}  ({len(apps)} no total)\n")
        print(f"  {'#':<5} {'Nome':<44} {'Versão'}")
        print("  " + "─" * 62)

        for idx in range(start, end):
            a       = apps[idx]
            name    = (a["name"][:41] + "...") if len(a["name"]) > 44 else a["name"]
            version = a["version"][:12] if a["version"] else "—"
            print(f"  {idx + 1:<5} {name:<44} {version}")

        print("\n  " + "─" * 62)
        print("  [número] Selecionar  |  [p] Próxima  |  [v] Anterior  |  [0] Voltar")

        choice = input("\n  Opção: ").strip().lower()

        if choice == "0":
            break
        elif choice == "p" and page < total_pages - 1:
            page += 1
        elif choice == "v" and page > 0:
            page -= 1
        elif choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(apps):
                _handle_uninstall(apps[idx])
            else:
                print("  ❌ Número inválido.")
                time.sleep(1)
        else:
            print("  ❌ Opção inválida.")
            time.sleep(1)


# ══════════════════════════════════════════════════════════════
# MENU PRINCIPAL
# ══════════════════════════════════════════════════════════════

def main_menu():
    """Loop principal com todas as opções unificadas."""
    while True:
        print_header()
        print("""
  Escolha uma opção:

    [1]  🎮  Game Mode         — DNS, plano de energia, matar processos pesados
    [2]  🗑️  Limpeza           — Temp, Lixeira, Windows Update, Prefetch
    [3]  📦  Deep Uninstaller  — Desinstalar apps e apagar todos os resquícios
    [4]  🚀  Tudo de Uma Vez   — Executa as 3 opções em sequência
    [0]  ❌  Sair
""")
        choice = input("  Opção: ").strip()

        if choice == "1":
            run_game_mode()
        elif choice == "2":
            run_junk_cleaner()
        elif choice == "3":
            run_deep_uninstaller()
        elif choice == "4":
            run_game_mode()
            run_junk_cleaner()
            run_deep_uninstaller()
        elif choice == "0":
            print("\n  👋 Encerrando. Até logo!\n")
            sys.exit(0)
        else:
            print("  ❌ Opção inválida.")
            time.sleep(1)


# ══════════════════════════════════════════════════════════════
# PONTO DE ENTRADA
# ══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    if os.name != "nt":
        print("❌ Este script é exclusivo para Windows.")
        sys.exit(1)

    if not is_admin():
        print("\n  ⚠️  AVISO: Execute como Administrador para acesso total.")
        print("     Clique com botão direito no arquivo → 'Executar como administrador'\n")
        input("  ENTER para continuar com acesso limitado...")

    main_menu()
