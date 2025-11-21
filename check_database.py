"""Check what's stored in the SQLite database."""
import sqlite3
import json
from pathlib import Path
import config

def check_database():
    """Display all exhibitions in the database."""
    db_path = config.DATABASE_PATH
    
    print("="*70)
    print("🗄️  CHECKING SQLITE DATABASE")
    print("="*70)
    
    # Check if database exists
    if not Path(db_path).exists():
        print(f"\n⚠️  Database not found at: {db_path}")
        print("   Database will be created when first exhibition is generated.")
        return
    
    print(f"\n📍 Database location: {db_path}")
    print(f"📦 Database size: {Path(db_path).stat().st_size / 1024:.2f} KB")
    
    # Connect to database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get table info
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    print(f"\n📊 Tables: {[t[0] for t in tables]}")
    
    # Count exhibitions
    cursor.execute("SELECT COUNT(*) FROM exhibitions")
    count = cursor.fetchone()[0]
    print(f"\n📚 Total exhibitions stored: {count}")
    
    if count == 0:
        print("\n   No exhibitions yet. Generate one to see it stored!")
        conn.close()
        return
    
    # List all exhibitions
    print("\n" + "-"*70)
    print("STORED EXHIBITIONS")
    print("-"*70)
    
    cursor.execute("""
        SELECT id, topic, title, created_at, quality_score
        FROM exhibitions
        ORDER BY created_at DESC
    """)
    
    exhibitions = cursor.fetchall()
    
    for i, (ex_id, topic, title, created_at, quality_score) in enumerate(exhibitions, 1):
        print(f"\n{i}. Exhibition ID: {ex_id}")
        print(f"   Topic: {topic}")
        print(f"   Title: {title[:60]}..." if title and len(title) > 60 else f"   Title: {title}")
        print(f"   Created: {created_at}")
        print(f"   Quality Score: {quality_score:.1%}" if quality_score else "   Quality Score: N/A")
    
    # Show detailed view of most recent
    if count > 0:
        print("\n" + "-"*70)
        print("MOST RECENT EXHIBITION (Detailed)")
        print("-"*70)
        
        cursor.execute("SELECT data FROM exhibitions ORDER BY created_at DESC LIMIT 1")
        data = cursor.fetchone()[0]
        exhibition = json.loads(data)
        
        print(f"\nTopic: {exhibition.get('topic')}")
        print(f"Title: {exhibition.get('title', 'N/A')}")
        print(f"Rooms: {len(exhibition.get('rooms', []))}")
        
        total_exhibits = sum(len(r.get('exhibits', [])) for r in exhibition.get('rooms', []))
        print(f"Total Exhibits: {total_exhibits}")
        print(f"Timeline Events: {len(exhibition.get('timeline', []))}")
        
        print("\nRooms:")
        for i, room in enumerate(exhibition.get('rooms', []), 1):
            print(f"  {i}. {room.get('title')}")
            print(f"     Exhibits: {len(room.get('exhibits', []))}")
    
    conn.close()
    
    print("\n" + "="*70)
    print("✅ DATABASE CHECK COMPLETE")
    print("="*70)
    
    print("\n💡 To view a specific exhibition:")
    print("   python view_exhibition.py <id>")
    
    print("\n💡 To clear the database:")
    print("   Delete the file: data/exhibitions.db")

if __name__ == "__main__":
    check_database()
