from datetime import datetime
from typing import Optional, Union

def format_datetime(dt: Union[str, int, float, datetime, None]) -> str:
    """Convertir une date ISO (2025-11-07T09:14:00) -> 07/11/2025 à 09h14."""
    if not dt:
        return "-"
    try:
        # Si c'est un datetime
        if isinstance(dt, datetime):
            dt_obj = dt
        # Si c'est un nombre
        elif isinstance(dt, (int, float)):
            dt_obj = datetime.fromtimestamp(dt)
        # Si c'est une chaîne
        elif isinstance(dt, str):
            s = dt.strip()
            dt_obj = None
            # 1) fromisoformat (gère "YYYY-MM-DD" et "YYYY-MM-DDTHH:MM:SS[.ffffff]")
            try:
                dt_obj = datetime.fromisoformat(s)
            except Exception:
                dt_obj = None
            # 2) essais explicites de formats courants
            if dt_obj is None:
                for fmt in ("%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
                    try:
                        dt_obj = datetime.strptime(s, fmt)
                        break
                    except Exception:
                        dt_obj = None
            # 3) si la chaîne est un timestamp numérique
            if dt_obj is None:
                try:
                    ts = float(s)
                    dt_obj = datetime.fromtimestamp(ts)
                except Exception:
                    dt_obj = None
            if dt_obj is None:
                # impossible de parser -> retourner la string d'origine
                return dt
        else:
            # type non géré -> renvoyer tel quel
            return str(dt)

        return dt_obj.strftime("%d/%m/%Y à %Hh%M")
    except Exception:
        return dt