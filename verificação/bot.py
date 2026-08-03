import asyncio
import os
import discord
from discord.ext import commands
from aiohttp import web

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ==================== CONFIGURAÇÕES ====================
# ID do canal de verificação atualizado
CANAL_VERIFICACAO_ID = 1525114015238455457

# ID do cargo atualizado que o usuário vai receber
CARGO_ID = 1525115321516560445

# O seu Client ID correto tirado do Developer Portal
CLIENT_ID = "1533627256524509286"
# ========================================================


# Classe do Botão de Verificação (Estilo Link limpo, sem emoji)
class BotaoVerificacao(discord.ui.View):

  def __init__(self):
    super().__init__(timeout=None)  # O botão nunca expira

    # URL gerada automaticamente usando o seu Client ID e o redirect configurado
    url_autorizacao = (
        f"https://discord.com/api/oauth2/authorize?client_id={CLIENT_ID}"
        "&redirect_uri=https%3A%2F%2Fdiscord.com&response_type=code&scope=identify%20guilds.join"
    )

    # Adiciona o botão de link sem emoji (mostrando apenas o texto e o ícone de link externo nativo)
    self.add_item(
        discord.ui.Button(
            label="Verificar Agora",
            style=discord.ButtonStyle.secondary,  # Botão cinza/clean
            url=url_autorizacao,
        )
    )


@bot.event
async def on_ready():
  print(f"Bot de Verificação conectado como {bot.user}!")
  bot.add_view(BotaoVerificacao())


# Comando para enviar o painel no canal configurado
@bot.command()
@commands.has_permissions(administrator=True)
async def painel(ctx):
  canal = bot.get_channel(CANAL_VERIFICACAO_ID)
  if not canal:
    await ctx.send("Canal de verificação não encontrado!")
    return

  embed = discord.Embed(
      title="Sistema de Verificação",
      description=(
          "Para acessar todos os canais do servidor e participar da comunidade, "
          "você precisa se verificar primeiro.\n\n**Como funciona:**\n"
          "• Clique no botão abaixo\n• Complete a autorização\n• Feche a aba do"
          " navegador e volte ao Discord!\n\nApós a verificação, você terá"
          " acesso completo ao servidor!"
      ),
      color=discord.Color.blue(),
  )
  embed.set_footer(text="Proteção e Segurança do Servidor")
  embed.set_image(
      url=(
          "https://cdn.discordapp.com/attachments/1491626518219198639/1533630932785827850/ChatGPT_Image_2_de_ago._de_2026_21_21_33.png?ex=6a71309b&is=6a6fdf1b&hm=0d4b7d09c69feb7d2b1d87229aeadfbb1b69feb9a2375249b79371d8fd59dc7b&"
      )
  )

  await canal.send(embed=embed, view=BotaoVerificacao())
  await ctx.send("Painel de verificação enviado com sucesso!", ephemeral=True)


# Servidor web simples para manter o Render ligado
async def handle(request):
  return web.Response(text="Bot de Verificação rodando com sucesso!")


async def start_web_server():
  app = web.Application()
  app.add_routes([web.get("/", handle)])
  runner = web.AppRunner(app)
  await runner.setup()
  port = int(os.environ.get("PORT", 10000))
  site = web.TCPSite(runner, "0.0.0.0", port)
  await site.start()


async def main():
  await start_web_server()

  # Token carregado de forma segura pelas Variáveis de Ambiente
  TOKEN = os.environ.get("DISCORD_TOKEN")

  if not TOKEN:
    print("Erro: Token não configurado nas variáveis de ambiente!")
    return
  await bot.start(TOKEN)


if __name__ == "__main__":
  asyncio.run(main())