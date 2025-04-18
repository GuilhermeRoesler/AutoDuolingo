from playwright.sync_api import sync_playwright

def main():
    try:
        with sync_playwright() as p:
            print("🚀 Iniciando navegador com perfil persistente...")
            
            # Cria contexto persistente com perfil salvo
            context = p.chromium.launch_persistent_context(
                user_data_dir=r"C:\Users\Gui\chrome_duolingo_profile",  # Caminho do seu perfil
                channel="chrome",
                headless=False,
                args=["--start-maximized"]
            )
            
            # Abre nova aba
            page = context.new_page()
            
            # Navega para o Duolingo
            page.goto("https://www.duolingo.com", wait_until="networkidle")
            
            print("\n🎥 MODO RECORDER ATIVADO")
            print("👉 Interaja com a página normalmente.")
            print("🧠 As ações geradas podem ser copiadas da aba DevTools (automação).")
            print("🛑 Pressione CTRL+C para encerrar quando terminar.\n")
            
            # Initial automation for test
            initial_automation()
            
            page.locator("[data-test=\"characters-nav\"]").click()
            page.get_by_role("link", name="Começar +10 XP").click()
            
            while page.locator("[data-test=\"player-next\"]").is_visible():
                print('GAY1')
                if page.get_by_role("button", name="1").is_visible():
                    buttons = page.get_by_role("button")
                    print(buttons)
                    print('GAY2')
                    break
                
                page.get_by_role("radio").nth(0).click()
                page.locator("[data-test=\"player-next\"]").click()
                page.locator("[data-test=\"player-next\"]").click()
            print('GAY3')
            
            # Ativa modo interativo do Playwright
            page.pause()
            
            # Fecha o contexto após o uso
            context.close()
    
    except Exception as e:
        print(f"❌ Erro durante a gravação: {str(e)}")

def initial_automation():
    ...

if __name__ == "__main__":
    main()
