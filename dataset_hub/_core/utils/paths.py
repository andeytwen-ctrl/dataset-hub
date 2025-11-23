from pathlib import Path
from dataset_hub._settings.loader import load_settings

def build_source_path(dataset_name: str, filename: str) -> Path:
    """
    Собирает путь к файлу датасета и создаёт необходимые директории.
    
    Параметры:
    - base_dir: базовая директория для всех датасетов
    - dataset_name: название датасета (например, 'titanic')
    - table_name: название таблицы или поддиректории
    - filename: имя файла, если None, берётся table_name
    
    Возвращает:
    - Полный Path к файлу
    """
    if filename is None:
        filename = table_name
        
    settings = load_settings()
    data_path = settings["data_path"]

    path = Path(data_path) / dataset_name
    path.mkdir(parents=True, exist_ok=True)
    
    return path / filename