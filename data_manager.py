"""
Centralized data manager for the Dash Montreal Crimes application
Optimizes performance by loading data only once and caching it
"""

import pandas as pd
import os
from functools import lru_cache
from typing import Optional, Dict, Any
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataManager:
    """
    Gestionnaire centralisé des données avec mise en cache
    """
    _instance = None
    _data_cache = {}
    _processed_cache = {}
    
    def __new__(cls):
        """Singleton pattern pour s'assurer qu'une seule instance existe"""
        if cls._instance is None:
            cls._instance = super(DataManager, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialisation du gestionnaire de données"""
        if not hasattr(self, 'initialized'):
            self.data_path = self._get_data_path()
            self.raw_data = None
            self.initialized = True
            logger.info("DataManager initialisé")
    
    def _get_data_path(self) -> str:
        """
        Détermine le chemin correct vers le fichier CSV
        """
       
        possible_paths = [
            "src/data/actes-criminels.csv",
            "data/actes-criminels.csv",
            "../data/actes-criminels.csv",
            os.path.join(os.path.dirname(__file__), "data", "actes-criminels.csv"),
            os.path.join(os.path.dirname(__file__), "..", "data", "actes-criminels.csv")
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                logger.info(f"Fichier CSV trouvé à: {path}")
                return path
        
       
        default_path = "src/data/actes-criminels.csv"
        logger.warning(f"Fichier CSV non trouvé, utilisation du chemin par défaut: {default_path}")
        return default_path
    
    def load_raw_data(self, force_reload: bool = False) -> pd.DataFrame:
        """
        Charge les données brutes du CSV avec mise en cache
        
        Args:
            force_reload: Force le rechargement des données même si elles sont en cache
            
        Returns:
            DataFrame contenant les données brutes
        """
        if self.raw_data is None or force_reload:
            try:
                logger.info(f"Chargement des données depuis: {self.data_path}")
                self.raw_data = pd.read_csv(self.data_path, parse_dates=["DATE"])
                logger.info(f"Données chargées: {len(self.raw_data)} lignes, {len(self.raw_data.columns)} colonnes")
                
               
                self._prepare_base_data()
                
            except Exception as e:
                logger.error(f"Erreur lors du chargement des données: {e}")
                raise
        
        return self.raw_data.copy()
    
    def _prepare_base_data(self):
        """
        Prépare les données de base (colonnes communes utilisées par plusieurs visualisations)
        """
        if self.raw_data is not None:
            self.raw_data["YEAR"] = self.raw_data["DATE"].dt.year
            self.raw_data["MONTH"] = self.raw_data["DATE"].dt.month
            self.raw_data["SEASON"] = self.raw_data["MONTH"] % 12 // 3 + 1
            
            season_map = {1: "Winter", 2: "Spring", 3: "Summer", 4: "Autumn"}
            self.raw_data["SEASON"] = self.raw_data["SEASON"].map(season_map)
            
            if 'QUART' in self.raw_data.columns:
                self.raw_data['QUART'] = self.raw_data['QUART'].str.lower()
                self.raw_data['DayOfWeek'] = self.raw_data['DATE'].dt.dayofweek
                self.raw_data['Day Type'] = self.raw_data['DayOfWeek'].apply(
                    lambda x: 'Weekend' if x >= 5 else 'Weekday'
                )
                
                time_labels = {
                    'jour': 'Day (09:01–16:00)',
                    'soir': 'Evening (16:01–00:00)',
                    'nuit': 'Night (00:01–08:00)'
                }
                self.raw_data['Time of Day'] = self.raw_data['QUART'].map(time_labels)
            
            logger.info("Données de base préparées avec colonnes temporelles")
    
    @lru_cache(maxsize=32)
    def get_filtered_data(self, 
                         start_year: Optional[int] = None,
                         end_year: Optional[int] = None,
                         pdq: Optional[int] = None,
                         category: Optional[str] = None) -> pd.DataFrame:
        """
        Retourne les données filtrées avec mise en cache LRU
        
        Args:
            start_year: Année de début (incluse)
            end_year: Année de fin (incluse)
            pdq: Numéro PDQ à filtrer
            category: Catégorie de crime à filtrer
            
        Returns:
            DataFrame filtré
        """
        cache_key = f"{start_year}_{end_year}_{pdq}_{category}"
        
        if cache_key in self._processed_cache:
            logger.debug(f"Données filtrées trouvées en cache: {cache_key}")
            return self._processed_cache[cache_key].copy()
        
       
        data = self.load_raw_data()
        
        if start_year is not None:
            data = data[data['YEAR'] >= start_year]
        if end_year is not None:
            data = data[data['YEAR'] <= end_year]
        if pdq is not None:
            data = data[data['PDQ'] == pdq]
        if category is not None:
            data = data[data['CATEGORIE'] == category]
        
        self._processed_cache[cache_key] = data.copy()
        logger.debug(f"Données filtrées mises en cache: {cache_key} ({len(data)} lignes)")
        
        return data.copy()
    
    def get_data_for_viz1(self) -> pd.DataFrame:
        """
        Retourne les données préparées pour la visualisation 1
        """
        return self.load_raw_data()
    
    def get_data_for_viz2(self) -> pd.DataFrame:
        """
        Retourne les données préparées pour la visualisation 2
        """
        return self.load_raw_data()
    
    def get_data_for_viz3(self) -> pd.DataFrame:
        """
        Retourne les données préparées pour la visualisation 3
        """
        return self.load_raw_data()
    
    def get_data_for_viz4(self) -> pd.DataFrame:
        """
        Retourne les données préparées pour la visualisation 4
        """
        return self.load_raw_data()
    
    def get_data_for_viz5(self) -> pd.DataFrame:
        """
        Retourne les données préparées pour la visualisation 5
        """
        return self.load_raw_data()
    
    def clear_cache(self):
        """
        Vide tous les caches
        """
        self._processed_cache.clear()
        self.get_filtered_data.cache_clear()
        logger.info("Cache vidé")
    
    def get_cache_info(self) -> Dict[str, Any]:
        """
        Retourne des informations sur l'état du cache
        """
        return {
            'processed_cache_size': len(self._processed_cache),
            'lru_cache_info': self.get_filtered_data.cache_info(),
            'data_loaded': self.raw_data is not None,
            'data_shape': self.raw_data.shape if self.raw_data is not None else None
        }

data_manager = DataManager()

def get_data() -> pd.DataFrame:
    """Fonction utilitaire pour obtenir les données brutes"""
    return data_manager.load_raw_data()

def get_filtered_data(**kwargs) -> pd.DataFrame:
    """Fonction utilitaire pour obtenir les données filtrées"""
    return data_manager.get_filtered_data(**kwargs)

def clear_data_cache():
    """Fonction utilitaire pour vider le cache"""
    data_manager.clear_cache()

