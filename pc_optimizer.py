"""
  Ω  GREEK OPTIMIZER  Σ
  Λ Δ Φ Ψ Π — Windows Performance & Optimization Tool
"""

import os
import sys
import shutil
import ctypes
import winreg
import tempfile
import subprocess
import time
import platform
import socket
from pathlib import Path
from datetime import datetime, timedelta
from itertools import zip_longest


# ══════════════════════════════════════════════════════════════
# CORES ANSI
# ══════════════════════════════════════════════════════════════

class C:
    RESET    = "\033[0m"
    BOLD     = "\033[1m"
    DIM      = "\033[2m"
    BLACK    = "\033[30m"
    RED      = "\033[31m"
    GREEN    = "\033[32m"
    YELLOW   = "\033[33m"
    BLUE     = "\033[34m"
    MAGENTA  = "\033[35m"
    CYAN     = "\033[36m"
    WHITE    = "\033[37m"
    BRED     = "\033[91m"
    BGREEN   = "\033[92m"
    BYELLOW  = "\033[93m"
    BBLUE    = "\033[94m"
    BMAGENTA = "\033[95m"
    BCYAN    = "\033[96m"
    BWHITE   = "\033[97m"

    @staticmethod
    def enable_ansi():
        try:
            kernel32 = ctypes.windll.kernel32
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
        except Exception:
            pass


def _c(color: str, text: str) -> str:
    return f"{color}{text}{C.RESET}"


# ══════════════════════════════════════════════════════════════
# TELA DE ABERTURA E ENCERRAMENTO
# ══════════════════════════════════════════════════════════════

# Logo GREEK OPTIMIZER em ASCII art (bloco grande)
LOGO = [
    r" ██████╗ ██████╗ ███████╗███████╗██╗  ██╗",
    r"██╔════╝ ██╔══██╗██╔════╝██╔════╝██║ ██╔╝",
    r"██║  ███╗██████╔╝█████╗  █████╗  █████╔╝ ",
    r"██║   ██║██╔══██╗██╔══╝  ██╔══╝  ██╔═██╗ ",
    r"╚██████╔╝██║  ██║███████╗███████╗██║  ██╗",
    r" ╚═════╝ ╚═╝  ╚═╝╚══════╝╚══════╝╚═╝  ╚═╝",
]


def show_startup():
    """Tela de abertura com logo grande. Aguarda ENTER para entrar no painel."""
    os.system("cls")

    admin_str = (f"{C.BGREEN}✓ Administrador{C.RESET}"
                 if is_admin() else f"{C.BYELLOW}⚠ Usuário Comum{C.RESET}")

    pad = "  "
    print()
    print()
    for line in LOGO:
        print(f"{pad}{C.BCYAN}{C.BOLD}{line}{C.RESET}")
    print()
    print(f"{pad}{C.BCYAN}{'━' * 44}{C.RESET}")
    print(f"{pad}{C.BWHITE}{C.BOLD}        O P T I M I Z E R{C.RESET}")
    print(f"{pad}{C.DIM}   Λ · Ω · Σ · Δ · Φ · Ψ · Π · Θ · Ξ · Γ{C.RESET}")
    print(f"{pad}{C.BCYAN}{'━' * 44}{C.RESET}")
    print()
    print(f"{pad}{C.DIM}Admin : {C.RESET}{admin_str}")
    print()
    print()
    input(f"{pad}{C.BCYAN}  ⚡  Pressione ENTER para acessar o painel...  ⚡{C.RESET}")


def show_exit_screen():
    """Tela de encerramento limpa."""
    os.system("cls")

    username = os.environ.get("USERNAME", "user")
    now_str  = datetime.now().strftime("%d/%m/%Y  %H:%M")

    pad = "  "
    print()
    print()
    for line in LOGO:
        print(f"{pad}{C.BYELLOW}{C.DIM}{line}{C.RESET}")
    print()
    print(f"{pad}{C.BYELLOW}{'━' * 44}{C.RESET}")
    print(f"{pad}{C.BYELLOW}{C.BOLD}        O P T I M I Z E R{C.RESET}")
    print(f"{pad}{C.BYELLOW}{'━' * 44}{C.RESET}")
    print()
    print(f"{pad}{C.BYELLOW}👋  Até logo, {username}!{C.RESET}")
    print(f"{pad}{C.DIM}📅  {now_str}{C.RESET}")
    print(f"{pad}{C.DIM}    Que Deus abençoe sua máquina!{C.RESET}")
    print()
    time.sleep(3)


# ══════════════════════════════════════════════════════════════
# UTILIDADES GERAIS
# ══════════════════════════════════════════════════════════════

def is_admin() -> bool:
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False


def confirm(prompt: str) -> bool:
    answer = input(
        f"\n  {C.CYAN}{prompt}{C.RESET} {C.DIM}[s/N]{C.RESET}: "
    ).strip().lower()
    return answer in ("s", "sim", "y", "yes")


def bytes_to_mb(size: int) -> float:
    return round(size / (1024 * 1024), 2)


def clear_screen():
    os.system("cls")


def print_header(subtitle: str = ""):
    clear_screen()
    print()
    print(f"  {C.BCYAN}{'━' * 60}{C.RESET}")
    print(f"  {C.BCYAN}{C.BOLD}  Ω  GREEK OPTIMIZER  Σ{C.RESET}"
          f"  {C.DIM}Λ · Δ · Φ · Ψ · Π · Θ{C.RESET}")
    if subtitle:
        print(f"  {C.CYAN}{'─' * 60}{C.RESET}")
        print(f"  {C.BOLD}{subtitle}{C.RESET}")
    mode = (f"{C.BGREEN}✅ Administrador{C.RESET}"
            if is_admin() else f"{C.BYELLOW}⚠️  Usuário comum (acesso limitado){C.RESET}")
    print(f"  {C.DIM}Admin: {C.RESET}{mode}")
    print(f"  {C.BCYAN}{'━' * 60}{C.RESET}")


def run_command(cmd: list, timeout: int = 120) -> tuple:
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return r.returncode, r.stdout + r.stderr
    except subprocess.TimeoutExpired:
        return -1, "Timeout."
    except Exception as e:
        return -1, str(e)


def clean_folder(folder: Path) -> tuple:
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
# MÓDULO 1 — GAME MODE
# ══════════════════════════════════════════════════════════════

HEAVY_PROCESSES = [
    "chrome.exe", "msedge.exe", "opera.exe", "brave.exe",
    "discord.exe", "skype.exe", "slack.exe", "teams.exe",
    "zoom.exe", "spotify.exe", "onedrive.exe", "outlook.exe",
]


def flush_dns():
    print(f"\n  {C.BCYAN}🌐 Limpando cache DNS...{C.RESET}")
    if not is_admin():
        print(f"  {C.BYELLOW}⚠️  Requer Administrador — pulado.{C.RESET}")
        return
    code, _ = run_command(["ipconfig", "/flushdns"])
    if code == 0:
        print(f"  {C.BGREEN}✅ Cache DNS limpo.{C.RESET}")
    else:
        print(f"  {C.BRED}❌ Falha ao limpar DNS.{C.RESET}")


def set_high_performance():
    print(f"\n  {C.BCYAN}⚡ Ativando plano de energia 'Alto Desempenho'...{C.RESET}")
    if not is_admin():
        print(f"  {C.BYELLOW}⚠️  Requer Administrador — pulado.{C.RESET}")
        return
    GUID = "8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c"
    code, _ = run_command(["powercfg", "/setactive", GUID])
    if code == 0:
        print(f"  {C.BGREEN}✅ Plano ativado.{C.RESET}")
    else:
        print(f"  {C.BRED}❌ Falha ao mudar plano de energia.{C.RESET}")


def kill_heavy_processes():
    print(f"\n  {C.BCYAN}🔫 Verificando processos pesados...{C.RESET}")
    code, output = run_command(["tasklist", "/fo", "csv", "/nh"])
    if code != 0:
        print(f"  {C.BRED}❌ Não foi possível listar processos.{C.RESET}")
        return

    running = [p for p in HEAVY_PROCESSES if p.lower() in output.lower()]
    if not running:
        print(f"  {C.BGREEN}✅ Nenhum processo pesado encontrado.{C.RESET}")
        return

    print(f"  {C.BYELLOW}Encontrados {len(running)} processo(s):{C.RESET}")
    for p in running:
        print(f"    {C.DIM}•{C.RESET} {p}")

    killed = 0
    for proc in running:
        if confirm(f"Encerrar '{proc}'?"):
            code, _ = run_command(["taskkill", "/f", "/im", proc])
            if code == 0:
                print(f"    {C.BGREEN}✅ '{proc}' encerrado.{C.RESET}")
                killed += 1
            else:
                print(f"    {C.BRED}❌ Não foi possível encerrar '{proc}'.{C.RESET}")
        else:
            print(f"    {C.DIM}⏭️  '{proc}' mantido.{C.RESET}")

    print(f"\n  {C.BCYAN}📊 {killed}/{len(running)} processos encerrados.{C.RESET}")


def run_game_mode():
    print_header("🎮  GAME MODE — Otimização para Jogos")
    flush_dns()
    set_high_performance()
    kill_heavy_processes()
    print(f"\n  {C.BGREEN}✅ Game Mode concluído! Bons jogos.{C.RESET}")
    input(f"\n  {C.DIM}Pressione ENTER para voltar ao menu...{C.RESET}")


# ══════════════════════════════════════════════════════════════
# MÓDULO 2 — LIMPEZA DE ARQUIVOS INÚTEIS
# ══════════════════════════════════════════════════════════════

WUPDATE_CACHE = Path(r"C:\Windows\SoftwareDistribution\Download")
PREFETCH_DIR  = Path(r"C:\Windows\Prefetch")


def _clean_recycle_bin() -> tuple:
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
    if not is_admin():
        print(f"  {C.BYELLOW}⚠️  Requer Administrador — pulado.{C.RESET}")
        return 0, 0
    os.system("net stop wuauserv >nul 2>&1")
    result = clean_folder(WUPDATE_CACHE)
    os.system("net start wuauserv >nul 2>&1")
    return result


def _clean_prefetch() -> tuple:
    if not is_admin():
        print(f"  {C.BYELLOW}⚠️  Requer Administrador — pulado.{C.RESET}")
        return 0, 0
    return clean_folder(PREFETCH_DIR)


JUNK_CATEGORIES = [
    ("%TEMP% do Sistema",       lambda: clean_folder(Path(tempfile.gettempdir()))),
    ("Lixeira",                 _clean_recycle_bin),
    ("Cache do Windows Update", _clean_windows_update),
    ("Prefetch do Windows",     _clean_prefetch),
]


def run_junk_cleaner():
    print_header("🗑️  LIMPEZA DE ARQUIVOS INÚTEIS")
    print()

    summary = []
    total_deleted, total_freed = 0, 0

    for name, func in JUNK_CATEGORIES:
        print(f"  {C.BCYAN}── {name}{C.RESET}")
        if not confirm(f"Limpar '{name}'?"):
            print(f"  {C.DIM}⏭️  Pulado.{C.RESET}\n")
            continue

        deleted, freed = func()
        freed_mb = bytes_to_mb(freed)
        total_deleted += deleted
        total_freed   += freed_mb
        summary.append((name, deleted, freed_mb))
        print(f"  {C.BGREEN}✅ {deleted} item(ns) | {freed_mb} MB liberados{C.RESET}\n")

    print(f"\n  {C.BCYAN}{'═' * 54}{C.RESET}")
    print(f"  {C.BOLD}📊 RESUMO DA LIMPEZA{C.RESET}")
    print(f"  {C.BCYAN}{'═' * 54}{C.RESET}")
    if not summary:
        print(f"  {C.DIM}Nenhuma categoria executada.{C.RESET}")
    else:
        W = 28
        print(f"  {C.CYAN}{'Categoria':<{W}} {'Itens':>6}  {'Liberado':>10}{C.RESET}")
        print(f"  {C.DIM}{'─' * 48}{C.RESET}")
        for cat, d, f in summary:
            print(f"  {cat:<{W}} {d:>6}  {C.BGREEN}{f:>8.2f} MB{C.RESET}")
        print(f"  {C.DIM}{'─' * 48}{C.RESET}")
        print(f"  {C.BOLD}{'TOTAL':<{W}} {total_deleted:>6}  {C.BGREEN}{total_freed:>8.2f} MB{C.RESET}")
    print(f"  {C.BCYAN}{'═' * 54}{C.RESET}")

    input(f"\n  {C.DIM}Pressione ENTER para voltar ao menu...{C.RESET}")


# ══════════════════════════════════════════════════════════════
# MÓDULO 3 — DEEP UNINSTALLER
# ══════════════════════════════════════════════════════════════

UNINSTALL_KEYS = [
    (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
    (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"),
    (winreg.HKEY_CURRENT_USER,  r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
]

LEFTOVER_DIRS = [
    Path(os.environ.get("APPDATA",      "")),
    Path(os.environ.get("LOCALAPPDATA", "")),
    Path(os.environ.get("LOCALAPPDATA", "")) / "Programs",
    Path(os.environ.get("PROGRAMDATA",  "")),
    Path(r"C:\Program Files"),
    Path(r"C:\Program Files (x86)"),
]

LEFTOVER_REG_ROOTS = [
    (winreg.HKEY_CURRENT_USER,  r"SOFTWARE"),
    (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE"),
    (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node"),
]


def _get_installed_apps() -> list:
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
    cmd_lower = cmd.lower()
    if "msiexec" in cmd_lower:
        cmd = cmd.replace("/I{", "/X{").replace("/i{", "/X{")
        if "/quiet" not in cmd_lower and "/q" not in cmd_lower:
            cmd += " /quiet /norestart"
    elif "uninst" in cmd_lower or "_uninstall" in cmd_lower:
        if "/s" not in cmd_lower:
            cmd += " /S"

    print(f"\n  {C.BCYAN}▶ Executando desinstalador...{C.RESET}")
    print(f"  {C.DIM}{cmd[:80]}{'...' if len(cmd) > 80 else ''}{C.RESET}")
    try:
        proc = subprocess.Popen(cmd, shell=True)
        proc.wait(timeout=180)
        return proc.returncode in (0, 1605, 1614, 3010)
    except subprocess.TimeoutExpired:
        proc.kill()
        print(f"  {C.BYELLOW}⚠️  Desinstalador não respondeu — processo encerrado.{C.RESET}")
        return False
    except Exception as e:
        print(f"  {C.BRED}❌ Erro: {e}{C.RESET}")
        return False


def _find_leftover_folders(app_name: str, install_location: str) -> list:
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
    hive_name = "HKLM" if hive == winreg.HKEY_LOCAL_MACHINE else "HKCU"
    run_command(["reg", "delete", f"{hive_name}\\{key_path}", "/f"])


def _deep_clean_app(app: dict):
    name             = app["name"]
    install_location = app.get("install_location", "")

    print(f"\n  {C.BCYAN}🔍 Procurando resquícios de '{name}'...{C.RESET}")
    time.sleep(1)

    folders = _find_leftover_folders(name, install_location)
    if folders:
        print(f"\n  {C.BYELLOW}📂 {len(folders)} pasta(s) residual(is) encontrada(s):{C.RESET}")
        for p in folders:
            try:
                size_mb = bytes_to_mb(sum(f.stat().st_size for f in p.rglob("*") if f.is_file()))
            except Exception:
                size_mb = 0.0
            print(f"    {C.DIM}•{C.RESET} {p}  ({size_mb} MB)")

        if confirm("  Apagar todas as pastas residuais?"):
            for p in folders:
                try:
                    shutil.rmtree(p, ignore_errors=True)
                    print(f"    {C.BGREEN}🗑️  Removido: {p.name}{C.RESET}")
                except Exception as e:
                    print(f"    {C.BYELLOW}⚠️  Erro ao remover '{p.name}': {e}{C.RESET}")
    else:
        print(f"  {C.BGREEN}✅ Nenhuma pasta residual encontrada.{C.RESET}")

    if is_admin():
        reg_keys = _find_leftover_registry(name)
        if reg_keys:
            print(f"\n  {C.BYELLOW}🗝️  {len(reg_keys)} chave(s) de registro encontrada(s):{C.RESET}")
            for _, path in reg_keys:
                print(f"    {C.DIM}•{C.RESET} {path}")
            if confirm("  Apagar essas chaves do registro?"):
                for hive, path in reg_keys:
                    _delete_registry_key(hive, path)
                    print(f"    {C.BGREEN}🗑️  Removido: ...\\{path.split(chr(92))[-1]}{C.RESET}")
        else:
            print(f"  {C.BGREEN}✅ Nenhuma chave de registro residual encontrada.{C.RESET}")
    else:
        print(f"\n  {C.BYELLOW}⚠️  Limpeza de registro ignorada (requer Administrador).{C.RESET}")


def _handle_uninstall(app: dict):
    print_header("📦  DEEP UNINSTALLER")
    print(f"\n  {C.BOLD}App selecionado:{C.RESET}\n")
    print(f"  {C.CYAN}Nome:      {C.RESET}{app['name']}")
    print(f"  {C.CYAN}Versão:    {C.RESET}{app['version'] or '—'}")
    print(f"  {C.CYAN}Fabricante:{C.RESET}{app['publisher'] or '—'}")
    if app["install_location"]:
        print(f"  {C.CYAN}Local:     {C.RESET}{app['install_location']}")
    print()

    if not confirm(f"Desinstalar '{app['name']}' completamente?"):
        print(f"  {C.DIM}⏭️  Cancelado.{C.RESET}")
        time.sleep(1)
        return

    print(f"\n  {C.BCYAN}── ETAPA 1: Desinstalação oficial ──{C.RESET}")
    success = _run_uninstaller(app["uninstall_cmd"])
    if success:
        print(f"  {C.BGREEN}✅ Desinstalador concluído.{C.RESET}")
    else:
        print(f"  {C.BYELLOW}⚠️  Desinstalador retornou erro. Prosseguindo com limpeza...{C.RESET}")

    print(f"\n  {C.BCYAN}── ETAPA 2: Remoção de Resquícios ──{C.RESET}")
    _deep_clean_app(app)

    print(f"\n  {C.BGREEN}✅ '{app['name']}' removido completamente!{C.RESET}")
    input(f"\n  {C.DIM}Pressione ENTER para voltar à lista...{C.RESET}")


def run_deep_uninstaller():
    print_header("📦  DEEP UNINSTALLER")
    print(f"\n  {C.DIM}Carregando aplicativos instalados...{C.RESET}\n")

    apps = _get_installed_apps()
    if not apps:
        print(f"  {C.BRED}❌ Nenhum aplicativo encontrado no registro.{C.RESET}")
        input(f"\n  {C.DIM}ENTER para voltar...{C.RESET}")
        return

    PAGE        = 20
    page        = 0
    total_pages = (len(apps) - 1) // PAGE + 1

    while True:
        print_header("📦  DEEP UNINSTALLER")
        start = page * PAGE
        end   = min(start + PAGE, len(apps))

        print(f"\n  {C.BCYAN}Apps instalados — Página {page + 1}/{total_pages}  ({len(apps)} no total){C.RESET}\n")
        print(f"  {C.CYAN}{'#':<5} {'Nome':<44} {'Versão'}{C.RESET}")
        print(f"  {C.DIM}{'─' * 62}{C.RESET}")

        for idx in range(start, end):
            a       = apps[idx]
            name    = (a["name"][:41] + "...") if len(a["name"]) > 44 else a["name"]
            version = a["version"][:12] if a["version"] else "—"
            print(f"  {C.DIM}{idx + 1:<5}{C.RESET} {name:<44} {C.DIM}{version}{C.RESET}")

        print(f"\n  {C.DIM}{'─' * 62}{C.RESET}")
        print(f"  {C.CYAN}[número]{C.RESET} Selecionar  {C.CYAN}[p]{C.RESET} Próxima"
              f"  {C.CYAN}[v]{C.RESET} Anterior  {C.CYAN}[0]{C.RESET} Voltar")

        choice = input(f"\n  {C.CYAN}Ω {C.RESET}Opção: ").strip().lower()

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
                print(f"  {C.BRED}❌ Número inválido.{C.RESET}")
                time.sleep(1)
        else:
            print(f"  {C.BRED}❌ Opção inválida.{C.RESET}")
            time.sleep(1)


# ══════════════════════════════════════════════════════════════
# MÓDULO 4 — LIMPEZA DE MÍDIA E DOWNLOADS
# ══════════════════════════════════════════════════════════════

PHOTO_EXT = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".heic", ".raw", ".tiff", ".tif"}
VIDEO_EXT = {".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm", ".m4v", ".3gp", ".mpeg"}
DOC_EXT   = {".zip", ".rar", ".7z", ".iso", ".msi", ".exe", ".tar", ".gz", ".pdf", ".docx"}

MEDIA_DIRS = {
    "Downloads": Path.home() / "Downloads",
    "Imagens":   Path.home() / "Pictures",
    "Vídeos":    Path.home() / "Videos",
    "Desktop":   Path.home() / "Desktop",
}


def _scan_files(folder: Path, extensions: set,
                min_days: int = 0, min_size_mb: float = 0) -> list:
    results = []
    if not folder.exists():
        return results
    cutoff    = datetime.now() - timedelta(days=min_days)
    min_bytes = min_size_mb * 1024 * 1024
    try:
        for f in folder.rglob("*"):
            if not f.is_file():
                continue
            if f.suffix.lower() not in extensions:
                continue
            try:
                stat  = f.stat()
                size  = stat.st_size
                mtime = datetime.fromtimestamp(stat.st_mtime)
                if min_days > 0 and mtime > cutoff:
                    continue
                if size < min_bytes:
                    continue
                results.append({"path": f, "size": size, "mtime": mtime, "name": f.name})
            except (PermissionError, OSError):
                continue
    except (PermissionError, OSError):
        pass
    return sorted(results, key=lambda x: x["size"], reverse=True)


def _print_file_table(files: list, max_rows: int = 20):
    print(f"\n  {C.CYAN}{'#':<5} {'Nome':<40} {'Tamanho':>10}  {'Data'}{C.RESET}")
    print(f"  {C.DIM}{'─' * 70}{C.RESET}")
    for i, f in enumerate(files[:max_rows], 1):
        name = (f["name"][:37] + "...") if len(f["name"]) > 40 else f["name"]
        mb   = bytes_to_mb(f["size"])
        date = f["mtime"].strftime("%d/%m/%Y")
        sc   = C.BRED if mb > 500 else (C.BYELLOW if mb > 100 else C.BWHITE)
        print(f"  {C.DIM}{i:<5}{C.RESET} {name:<40} {sc}{mb:>8.1f} MB{C.RESET}  {C.DIM}{date}{C.RESET}")
    if len(files) > max_rows:
        print(f"  {C.DIM}... e mais {len(files) - max_rows} arquivo(s){C.RESET}")
    total_mb = bytes_to_mb(sum(f["size"] for f in files))
    print(f"  {C.DIM}{'─' * 70}{C.RESET}")
    print(f"  {C.BOLD}Total: {len(files)} arquivo(s) → {C.BGREEN}{total_mb:.1f} MB{C.RESET}")


def _do_delete(files: list):
    deleted, freed = 0, 0
    for f in files:
        try:
            freed += f["size"]
            f["path"].unlink()
            deleted += 1
        except (PermissionError, OSError):
            pass
    print(f"\n  {C.BGREEN}✅ {deleted} arquivo(s) removido(s) — {bytes_to_mb(freed):.1f} MB liberados!{C.RESET}")


def _clean_old_downloads():
    print_header("📥  DOWNLOADS ANTIGOS")
    folder = MEDIA_DIRS["Downloads"]
    print(f"\n  {C.DIM}Pasta: {folder}{C.RESET}")

    try:
        days_str = input(f"\n  {C.CYAN}Arquivos mais antigos que quantos dias? [30]: {C.RESET}").strip()
        days = int(days_str) if days_str.isdigit() else 30
    except Exception:
        days = 30

    all_exts = PHOTO_EXT | VIDEO_EXT | DOC_EXT | {".txt", ".csv", ".xlsx", ".pptx"}
    print(f"\n  {C.DIM}Procurando arquivos com mais de {days} dias...{C.RESET}")
    files = _scan_files(folder, all_exts, min_days=days)

    if not files:
        print(f"\n  {C.BGREEN}✅ Nenhum arquivo encontrado com mais de {days} dias.{C.RESET}")
        input(f"\n  {C.DIM}ENTER para voltar...{C.RESET}")
        return

    _print_file_table(files)

    if confirm("Apagar TODOS esses arquivos?"):
        _do_delete(files)
    else:
        print(f"  {C.DIM}⏭️  Cancelado.{C.RESET}")

    input(f"\n  {C.DIM}ENTER para voltar...{C.RESET}")


def _clean_photos():
    print_header("🖼️  LIMPEZA DE FOTOS")
    print(f"\n  {C.DIM}Procurando fotos em Downloads e Imagens...{C.RESET}")

    all_photos = []
    for fname, folder in [("Downloads", MEDIA_DIRS["Downloads"]),
                           ("Imagens",   MEDIA_DIRS["Imagens"])]:
        found = _scan_files(folder, PHOTO_EXT)
        for f in found:
            f["folder"] = fname
        all_photos.extend(found)

    if not all_photos:
        print(f"\n  {C.BGREEN}✅ Nenhuma foto encontrada.{C.RESET}")
        input(f"\n  {C.DIM}ENTER para voltar...{C.RESET}")
        return

    _print_file_table(all_photos)
    total_mb = bytes_to_mb(sum(f["size"] for f in all_photos))

    print(f"\n  {C.CYAN}Opções:{C.RESET}")
    print(f"    {C.BCYAN}[1]{C.RESET} Apagar todas as fotos ({total_mb:.1f} MB)")
    print(f"    {C.BCYAN}[2]{C.RESET} Apagar apenas de Downloads")
    print(f"    {C.DIM}[0]{C.RESET} Cancelar")

    choice = input(f"\n  {C.CYAN}Ω {C.RESET}Opção: ").strip()

    if choice == "1":
        if confirm(f"Apagar {len(all_photos)} foto(s)?"):
            _do_delete(all_photos)
    elif choice == "2":
        to_del = [f for f in all_photos if f.get("folder") == "Downloads"]
        if to_del and confirm(f"Apagar {len(to_del)} foto(s) de Downloads?"):
            _do_delete(to_del)
    else:
        print(f"  {C.DIM}⏭️  Cancelado.{C.RESET}")

    input(f"\n  {C.DIM}ENTER para voltar...{C.RESET}")


def _clean_videos():
    print_header("🎬  LIMPEZA DE VÍDEOS GRANDES")

    try:
        size_str = input(f"\n  {C.CYAN}Vídeos maiores que quantos MB? [200]: {C.RESET}").strip()
        min_size = float(size_str) if size_str.replace(".", "").isdigit() else 200.0
    except Exception:
        min_size = 200.0

    print(f"\n  {C.DIM}Procurando vídeos maiores que {min_size:.0f} MB...{C.RESET}")
    all_videos = []
    for folder in [MEDIA_DIRS["Downloads"], MEDIA_DIRS["Vídeos"], MEDIA_DIRS["Desktop"]]:
        all_videos.extend(_scan_files(folder, VIDEO_EXT, min_size_mb=min_size))

    if not all_videos:
        print(f"\n  {C.BGREEN}✅ Nenhum vídeo grande encontrado.{C.RESET}")
        input(f"\n  {C.DIM}ENTER para voltar...{C.RESET}")
        return

    _print_file_table(all_videos)

    if confirm("Apagar TODOS esses vídeos?"):
        _do_delete(all_videos)
    else:
        print(f"  {C.DIM}⏭️  Cancelado.{C.RESET}")

    input(f"\n  {C.DIM}ENTER para voltar...{C.RESET}")


def run_media_cleaner():
    while True:
        print_header("📁  LIMPEZA DE MÍDIA E DOWNLOADS")
        print(f"""
  {C.DIM}Escolha o que deseja limpar:{C.RESET}

    {C.BCYAN}[1]{C.RESET}  📥  Downloads Antigos   — Arquivos com mais de X dias
    {C.BCYAN}[2]{C.RESET}  🖼️   Fotos               — Imagens em Downloads e Pictures
    {C.BCYAN}[3]{C.RESET}  🎬  Vídeos Grandes       — Vídeos acima de X MB
    {C.BCYAN}[4]{C.RESET}  🔥  Limpar Tudo          — Executa as 3 opções acima
    {C.DIM}[0]{C.RESET}  ↩️   Voltar ao Menu
""")
        choice = input(f"  {C.CYAN}Ω {C.RESET}Opção: ").strip()

        if choice == "1":
            _clean_old_downloads()
        elif choice == "2":
            _clean_photos()
        elif choice == "3":
            _clean_videos()
        elif choice == "4":
            _clean_old_downloads()
            _clean_photos()
            _clean_videos()
        elif choice == "0":
            break
        else:
            print(f"  {C.BRED}❌ Opção inválida.{C.RESET}")
            time.sleep(1)


# ══════════════════════════════════════════════════════════════
# MENU PRINCIPAL
# ══════════════════════════════════════════════════════════════

def main_menu():
    while True:
        print_header()
        now = datetime.now().strftime("%d/%m/%Y  %H:%M")
        print(f"""
  {C.DIM}Escolha uma opção:{C.RESET}

    {C.BCYAN}[1]{C.RESET}  🎮  {C.BOLD}Game Mode{C.RESET}          — DNS, plano de energia, processos pesados
    {C.BCYAN}[2]{C.RESET}  🗑️  {C.BOLD}Limpeza{C.RESET}            — Temp, Lixeira, Windows Update, Prefetch
    {C.BCYAN}[3]{C.RESET}  📦  {C.BOLD}Deep Uninstaller{C.RESET}   — Desinstalar apps e apagar resquícios
    {C.BCYAN}[4]{C.RESET}  📁  {C.BOLD}Mídia & Downloads{C.RESET}  — Fotos, vídeos e arquivos antigos
    {C.BCYAN}[5]{C.RESET}  🚀  {C.BOLD}Otimização Total{C.RESET}   — Executa todas as opções em sequência
    {C.DIM}[0]{C.RESET}  ❌  {C.BOLD}Sair{C.RESET}

  {C.DIM}─────────────────────────────────────{C.RESET}
  {C.DIM}🕐 {now}{C.RESET}
""")
        choice = input(f"  {C.BCYAN}Ω{C.RESET} Opção: ").strip()

        if choice == "1":
            run_game_mode()
        elif choice == "2":
            run_junk_cleaner()
        elif choice == "3":
            run_deep_uninstaller()
        elif choice == "4":
            run_media_cleaner()
        elif choice == "5":
            run_game_mode()
            run_junk_cleaner()
            run_media_cleaner()
            run_deep_uninstaller()
        elif choice == "0":
            show_exit_screen()
            print(f"\n  {C.BYELLOW}👋 Que Deus abençoe! Até logo!{C.RESET}\n")
            sys.exit(0)
        else:
            print(f"  {C.BRED}❌ Opção inválida.{C.RESET}")
            time.sleep(1)


# ══════════════════════════════════════════════════════════════
# PONTO DE ENTRADA
# ══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    if os.name != "nt":
        print("❌ Este script é exclusivo para Windows.")
        sys.exit(1)

    C.enable_ansi()
    show_startup()
    main_menu()
