"""Memory Bank Agent - stores and retrieves exhibitions."""
import json
import sqlite3
from typing import Dict, List, Optional
from datetime import datetime
from pathlib import Path
from agents.base_agent import BaseAgent
import config

class MemoryBankAgent(BaseAgent):
    """Agent that manages exhibition storage and retrieval."""
    
    def __init__(self):
        super().__init__("MemoryBankAgent")
        self.db_path = config.DATABASE_PATH
        self._init_database()
    
    def _init_database(self):
        """Initialize SQLite database."""
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS exhibitions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic TEXT NOT NULL,
                title TEXT,
                created_at TEXT,
                quality_score REAL,
                data TEXT NOT NULL
            )
        """)
        
        conn.commit()
        conn.close()
    
    def _process(self, input_data: Dict) -> Dict:
        """
        Store exhibition in memory bank.
        
        Args:
            input_data: Exhibition data with evaluation
            
        Returns:
            Storage confirmation with ID
        """
        exhibition = input_data.get("exhibition", {})
        evaluation = input_data.get("evaluation", {})
        
        # Store in database
        exhibition_id = self._store_exhibition(exhibition, evaluation)
        
        # Save JSON file
        self._save_exhibition_file(exhibition, exhibition_id)
        
        return {
            "exhibition_id": exhibition_id,
            "stored": True,
            "topic": exhibition.get("topic", "")
        }
    
    def _store_exhibition(self, exhibition: Dict, evaluation: Dict) -> int:
        """Store exhibition in database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO exhibitions (topic, title, created_at, quality_score, data)
            VALUES (?, ?, ?, ?, ?)
        """, (
            exhibition.get("topic", ""),
            exhibition.get("title", ""),
            datetime.now().isoformat(),
            evaluation.get("overall_score", 0.0),
            json.dumps(exhibition)
        ))
        
        exhibition_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return exhibition_id
    
    def _save_exhibition_file(self, exhibition: Dict, exhibition_id: int):
        """Save exhibition as JSON file."""
        Path(config.EXHIBITIONS_DIR).mkdir(parents=True, exist_ok=True)
        
        filename = f"exhibition_{exhibition_id}_{exhibition.get('topic', 'unknown').replace(' ', '_')}.json"
        filepath = Path(config.EXHIBITIONS_DIR) / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(exhibition, f, indent=2, ensure_ascii=False)
    
    def retrieve_exhibition(self, exhibition_id: int) -> Optional[Dict]:
        """Retrieve exhibition by ID."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT data FROM exhibitions WHERE id = ?", (exhibition_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return json.loads(row[0])
        return None
    
    def list_exhibitions(self, limit: int = 10) -> List[Dict]:
        """List recent exhibitions."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, topic, title, created_at, quality_score
            FROM exhibitions
            ORDER BY created_at DESC
            LIMIT ?
        """, (limit,))
        
        exhibitions = []
        for row in cursor.fetchall():
            exhibitions.append({
                "id": row[0],
                "topic": row[1],
                "title": row[2],
                "created_at": row[3],
                "quality_score": row[4]
            })
        
        conn.close()
        return exhibitions
