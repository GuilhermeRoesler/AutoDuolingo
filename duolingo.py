from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
import logging
import os

class Duolingo:
    """
    Classe para automatizar interações com o Duolingo usando Playwright.
    Permite login automático e completar lições automaticamente.
    """
    
    def __init__(self, user_data_dir=None, headless=False, timeout=60000):
        """
        Inicializa a classe Duolingo.
        
        Args:
            user_data_dir (str): Diretório para o perfil do Chrome. Se None, usa o padrão.
            headless (bool): Se True, executa o navegador em modo headless.
            timeout (int): Tempo limite em ms para operações de navegação.
        """
        self.user_data_dir = user_data_dir or os.path.join(os.path.expanduser("~"), "chrome_duolingo_profile")
        self.headless = headless
        self.timeout = timeout
        self.playwright = None
        self.context = None
        self.page = None
        
        # Configurar logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%T-%m-%d %H:%M:%S'
        )
        self.logger = logging.getLogger(__name__)
    
    def start(self):
        """Inicia o navegador e configura o contexto."""
        self.playwright = sync_playwright().start()
        
        try:
            self.logger.info("Iniciando navegador Chrome...")
            self.context = self.playwright.chromium.launch_persistent_context(
                user_data_dir=self.user_data_dir,
                channel="chrome",
                headless=self.headless,
                args=[
                    "--start-maximized",
                    "--disable-blink-features=AutomationControlled"
                ],
                ignore_default_args=["--enable-automation"],
                timeout=self.timeout
            )
            
            self.page = self.context.new_page()
            self.logger.info("Navegador iniciado com sucesso.")
            return True
        except Exception as e:
            self.logger.error(f"Erro ao iniciar o navegador: {e}")
            self.close()
            return False
    
    def navigate_to_duolingo(self):
        """Navega para o site do Duolingo e verifica o login"""
        try:
            self.logger.info("Navegando para o Duolingo...")
            self.page.goto("https://www.duolingo.com/", wait_until="networkidle")
            
            # Verifica se já está logado
            if self.page.locator("[data-test='have-account']").is_visible():
                self.logger.warning("⚠️ Ainda não está logado. Faça login MANUALMENTE uma vez.")
                input("Pressione Enter após logar...")
            else:
                self.logger.info("✅ Login automático funcionou!")
            
            return True
        except Exception as e:
            self.logger.error(f"Erro ao navegar para o Duolingo: {e}")
            return False
    
    def start_lesson(self):
        """Inicia uma lição de caracteres"""
        try:
            self.logger.info("Iniciando lição de caracteres...")
            self.page.locator("[data-test='characters-nav']").click()
            self.page.get_by_role("link", name="Começar +10 XP").click()
            return True
        except Exception as e:
            self.logger.error(f"Erro ao iniciar a lição: {e}")
            return False
    
    def complete_lesson(self):
        """Completa uma lição inteira automaticamente."""
        try:
            self.logger.info("Aguardando botão 'next' ficar visível...")
            self.page.locator("[data-test='player-next']").wait_for(state="visible", timeout=30000)
            self.logger.info("Botão 'next' encontrado. Iniciando o loop de lição...")
            
            answer_index = 0
            while True:
                # Verifica se o botão 'next' ainda está visível
                if not self.page.locator("[data-test='player-next']").is_visible(timeout=10000):
                    self.logger.info("Botão 'next' não está mais visível. Lição concluída!")
                    break
                
                # Verifica se o exercício é normal
                # if self.page.get_by_role("radio").nth(0).is_visible():
                # if self.page.get_by_text("O que você escuta?").is_visible() or self.page.get_by_text("Ouça e responda:").is_visible():
                if self.page.query_selector('div._308fG._1vQbM._1iLiY[aria-label="choice"]') or self.page.query_selector('div.PaKCO._1vQbM[aria-label="choice"]'):
                    self.handle_normal_exercise(answer_index)
                    continue
                
                # Verifica se o exercício é de fala
                if self.page.get_by_role("button", name="Clique para falar").is_visible(timeout=10000):
                    self.handle_speaking_exercise()
                    continue
                
                # Verifica se o exercício é especial
                # if self.page.get_by_role("button", name="4").is_visible(timeout=10000):
                # if self.page.get_by_text("Combine os pares:").is_visible():
                if self.page.query_selector('div._2P2RV._1bmNz._3rat3'):
                    self.handle_especial_exercise()
                    answer_index = 1
                    continue
                
                self.finish_lesson()
                break
            
            return True
        except PlaywrightTimeoutError:
            self.logger.error("Timeout esperando pelo botão 'next'")
            return False
        except Exception as e:
            self.logger.error(f"Erro ao completar a lição: {str(e)}")
            return False
    
    def handle_speaking_exercise(self):
        """Lida com exercícios de fala, pulando-os"""
        try:
            self.logger.info("Pulando exercício de fala...")
            self.skip_exercise()
            return True
        except Exception as e:
            self.logger.error(f"Erro ao completar exercício de fala: {str(e)}")
            return False
    
    def handle_especial_exercise(self):
        """Lida com lições especiais que têm botões numerados"""
        try:
            self.logger.info("Pulando lição especial...")
            self.skip_exercise()
            return True
        except Exception as e:
            self.logger.error(f"Erro ao completar exercício especial: {str(e)}")
            return False
    
    def handle_normal_exercise(self, answer_index=0):
        """
        Completa um exercício normal de múltipla escolha.
        
        Args:
            answer_index (int): Índice da resposta a ser selecionada (padrão: 0)
        """
        try:
            self.logger.info(f"Respondendo exercício normal com opção {answer_index}...")
            self.page.get_by_role("radio").nth(answer_index).click()
            self.next_exercise()
            return True
        except Exception as e:
            self.logger.error(f"Erro ao responder exercício normal: {str(e)}")
            return False
    
    def finish_lesson(self):
        self.logger.info("Encerrando lição...")
        while True:
            if self.page.locator("[data-test='player-next']").is_visible(timeout=10000):
                self.page.locator("[data-test='player-next']").click()
            else:
                self.logger.info("Botão 'next' não está mais visível. Lição concluída!")
                break
    
    def run(self):
        """Executa o fluxo completo de automação do Duolingo."""
        try:
            if not self.start():
                return False
            
            if not self.navigate_to_duolingo():
                return False
            
            if not self.start_lesson():
                return False
            
            if not self.complete_lesson():
                return False
            
            self.logger.info("Lição concluída com sucesso!")
            input("Pressione Enter para encerrar...")
            return True
        except Exception as e:
            self.logger.error(f"Erro ao executar o fluxo: {str(e)}")
            return False
        finally:
            self.close()
    
    def close(self):
        """Fecha o navegador e libera recursos."""
        try:
            if self.context:
                self.context.close()
            if self.playwright:
                self.playwright.stop()
            self.logger.info("Recursos liberados")
        except Exception as e:
            self.logger.error(f"Erro ao fechar recursos: {str(e)}")
    
    def skip_exercise(self):
        self.page.locator("[data-test='player-skip']").click()
        self.page.locator("[data-test='player-next']").click()
    
    def next_exercise(self):
        self.page.locator("[data-test='player-next']").click()
        self.page.locator("[data-test='player-next']").click()

if __name__ == "__main__":
    duolingo = Duolingo()
    duolingo.run()