import requests
import threading
import time
from src.utils import Logger, GameSettings

POLL_INTERVAL = 0.02 #每次迴圈等待 0.02 秒就嘗試一次 fetch。
#大多數情況應該放慢（例如 0.1~0.5s 或更久），以減少網路/CPU 負擔。


#向伺服器註冊（register()）取得 player_id
#週期性地向伺服器查詢其他玩家清單（背景執行緒 _loop() → _fetch_players()）。
#需要時送出自己位置更新（update(x,y,map_name)）
class OnlineManager:
    list_players: list[dict]
    player_id: int
    
    #self._thread / self._stop_event：用來啟動/停止輪詢執行緒。
    _stop_event: threading.Event
    _thread: threading.Thread | None
    #self._lock：保護 self.list_players 的讀寫
    _lock: threading.Lock
    
    def __init__(self):             #在setting.py
        self.base: str = GameSettings.ONLINE_SERVER_URL #伺服器 base URL
        self.player_id = -1 #預設未註冊
        self.list_players = []

        self._thread = None
        self._stop_event = threading.Event()
        self._lock = threading.Lock()
        
        Logger.info("OnlineManager initialized")
        
    def enter(self):
        self.register()
        self.start()
            
    def exit(self):
        self.stop()
        
    def get_list_players(self) -> list[dict]:
        with self._lock:
            return list(self.list_players)

    # ------------------------------------------------------------------
    # Threading and API Calling Below
    # ------------------------------------------------------------------
    def register(self):
        try:
            url = f"{self.base}/register"
            resp = requests.get(url, timeout=5)
            resp.raise_for_status() #若 HTTP error（4xx/5xx）會丟出例外
            data = resp.json()
            if resp.status_code == 200:
                self.player_id = data["id"]
                Logger.info(f"OnlineManager registered with id={self.player_id}")
            else:
                Logger.error("Registration failed:", data)
        except Exception as e:
            Logger.warning(f"OnlineManager registration error: {e}")
        return

    def update(self, x: float, y: float, map_name: str) -> bool:
        if self.player_id == -1:
            # Try to register again
            return False
        
        url = f"{self.base}/players"
        body = {"id": self.player_id, "x": x, "y": y, "map": map_name}
        try:
                    #傳送json形式的玩家資訊
            resp = requests.post(url, json=body, timeout=5)
            if resp.status_code == 200:
                return True
            Logger.warning(f"Update failed: {resp.status_code} {resp.text}")
        except Exception as e:
            if self._on_error:
                try:
                    self._on_error(e)
                except Exception:
                    pass
            Logger.warning(f"Online update error: {e}")
        return False

    def start(self) -> None:
        if self._thread and self._thread.is_alive():
            return
        self._stop_event.clear()
        self._thread = threading.Thread(
            target=self._loop,
            name="OnlineManagerPoller",
            daemon=True
        )
        self._thread.start()

    def stop(self) -> None:
        self._stop_event.set()
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=2)

    def _loop(self) -> None:
        while not self._stop_event.wait(POLL_INTERVAL):
            self._fetch_players()
            
    def _fetch_players(self) -> None:
        try:
            url = f"{self.base}/players"
            resp = requests.get(url, timeout=5)
            resp.raise_for_status()
            all_players = resp.json().get("players", [])

            pid = self.player_id
            filtered = [p for key, p in all_players.items() if int(key) != pid]
            with self._lock:
                self.list_players = filtered
            
        except Exception as e:
            Logger.warning(f"OnlineManager fetch error: {e}")