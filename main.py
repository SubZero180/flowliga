import discord
import asyncio
from discord.ext import commands

# Bot-Intents definieren
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.members = True  # Hinzugefügt, um Member Join Event zu überwachen

# Bot initialisieren
bot = commands.Bot(command_prefix='^^', intents=intents)


# Event, wenn der Bot bereit ist
@bot.event
async def on_ready():
  print(f"Bot {bot.user.name} wurde gestartet und ist online!")


# Testbefehl zum Prüfen der Verbindung
@bot.command()
async def ping(ctx):
  await ctx.send('pong')


# Funktion zum Zuweisen von Rollen zu Usern
@bot.command(name='joingroup')
async def assign_role(ctx, group_num: int, *members: discord.Member):
  role_name = f'Gruppe-{group_num}'
  role = discord.utils.get(ctx.guild.roles, name=role_name)

  if role is not None:
    for member in members:
      await member.add_roles(role)
      await ctx.send(f'{member.mention} wurde {role.name} zugewiesen.')
  else:
    await ctx.send(
      f'Die Rolle Gruppe-{group_num} konnte nicht gefunden werden.')


# Funktion zum Erneuern mehrerer Kanäle
@bot.command(name='refresh')
async def refresh_channels(ctx, max_group: int):
  # Iterate über alle Gruppen
  for i in range(1, max_group + 1):
    channel_name = f'👥┃gruppe-{i}'
    channel = discord.utils.get(ctx.guild.text_channels, name=channel_name)

    if channel:
      # Klone den Kanal
      new_channel = await channel.clone()

      # Warten, um sicherzustellen, dass der Kanal vollständig geklont ist
      await asyncio.sleep(3)

      # Lösche den alten Kanal
      await channel.delete()

      # Senden der Begrüßungsnachricht im neuen Kanal
      message = await new_channel.send(
        "🎉 **HERZLICH WILLKOMMEN** 🎊 \n\n"
        "Dies ist der Chat deiner 👥 **Gruppe**. \n"
        "Hier kannst du nun die **Spieltermine** für die aktuelle Phase vereinbaren. \n"
        "Die **Spielberichte** postest du einfach über unser **[Berichte-Tool](http://bericht.flowliga.de)** \n"
        "Die Lidartsnamen deiner Gegner findest du unter **[LIDARTS-NAMEN](https://airtable.com/appkv4DB0aRincTXP/shrJYuXXRGrB4KGI0)**\n"
        "Wir wünschen Dir und deiner Gruppe viel Spaß und **Good Darts**! 🎯💪\n\n"
        "**DEADLINE** für die **Spielberichte** ist der **01. Oktober 2024 um 12:00 UHR (3 WOCHEN)**.\n"
        "Alle bis dahin **nicht** abgegeben Spielberichte werden **automatisch als 0:0** gewertet."
      )

      # Pinne die Nachricht an
      await message.pin()

      # Bestätigungsnachricht im Ausgangskanal
      await ctx.send(f'Kanal {channel_name} wurde aktualisiert und erneuert.')
    else:
      await ctx.send(f'Kanal {channel_name} konnte nicht gefunden werden.')


# Neue Funktion zum Entfernen von Rollen von Mitgliedern
@bot.command(name='groupdel')
async def groupdel(ctx, group_num: int):
  for i in range(1, group_num + 1):
    role = discord.utils.get(ctx.guild.roles, name=f'Gruppe-{i}')
    if role is not None:
      for member in role.members:
        await member.remove_roles(role)
        await ctx.send(f'{member.mention} wurde {role.name} entzogen.')
    else:
      await ctx.send(f'Die Rolle Gruppe-{i} konnte nicht gefunden werden.')


# Bot starten
bot.run(
  'BOT-API')
