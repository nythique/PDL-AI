import os
import logging
import wavelink
import colorama

from colorama import Fore, Style
from typing import Optional, List
from config.settings import SECURITY_LOG_PATH, ERROR_LOG_PATH
from config.settings import LAVALINK_HOST1, LAVALINK_PORT1, LAVALINK_PWDS1
from config.settings import LAVALINK_HOST2, LAVALINK_PORT2, LAVALINK_PWDS2
from config.settings import LAVALINK_HOST3, LAVALINK_PORT3, LAVALINK_PWDS3

info_handler = logging.FileHandler(settings.SECURITY_LOG_PATH, encoding='utf-8')
info_handler.setLevel(logging.INFO)
info_handler.setFormatter(logging.Formatter(
    '[%(levelname)s] %(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S'
))
error_handler = logging.FileHandler(settings.ERROR_LOG_PATH, encoding='utf-8')
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(logging.Formatter(
    '[%(levelname)s] %(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S'
))
logging.getLogger().handlers = []
logging.getLogger().addHandler(info_handler)
logging.getLogger().addHandler(error_handler)
logging.getLogger().setLevel(logging.INFO)
colorama.init()

class LavalinkManager:
    def __init__(self):
        self.nodes: List[wavelink.Node] = []
        self.current_node: Optional[wavelink.Node] = None
        self.servers = [
            {
                "host": LAVALINK_HOST1,
                "port": int(LAVALINK_PORT1),
                "password": LAVALINK_PWDS1
            },
            {
                "host": LAVALINK_HOST2,
                "port": int(LAVALINK_PORT2),
                "password": LAVALINK_PWDS2 
            },
            {
                "host": LAVALINK_HOST3,
                "port": int(LAVALINK_PORT3),
                "password": LAVALINK_PWDS3
            }
        ]

    async def connect_nodes(self, bot):

        await bot.wait_until_ready()
        
        for server in self.servers:
            try:
                node = await wavelink.NodePool.create_node(
                    bot=bot,
                    host=server["host"],
                    port=server["port"],
                    password=server["password"]
                )
                self.nodes.append(node)
                if not self.current_node:
                    self.current_node = node
                logging.info(f"[LAVALINK] Connecté au serveur: {server['host']}")
            except Exception as e:
                logging.error(f"[LAVALINK] Erreur de connexion à {server['host']}: {e}")

    async def get_best_node(self) -> Optional[wavelink.Node]:
        if not self.nodes:
            return None
        
        # Choisit le nœud avec le moins de charge
        available_nodes = [node for node in self.nodes if node.is_available]
        if not available_nodes:
            return None
            
        return min(available_nodes, key=lambda n: n.stats.playing_players)

    async def get_player(self, guild_id: int) -> Optional[wavelink.Player]:
        """
        NOTE: Obtient un player pour un serveur spécifique.
        Si aucun nœud n'est disponible, retourne None.
        """
        node = await self.get_best_node()
        if not node:
            return None
        return await node.get_player(guild_id)