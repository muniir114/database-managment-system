import sqlite3
from tabulate import tabulate

class DatabaseEditor:
    def __init__(self):
        self.conn = None
        self.cur = None
    
    def connect(self):
        """Connect to an existing database or create a new one"""
        while True:
            db_file = input("Enter database filename (e.g., school.db): ")
            if not db_file:
                print("⚠️ Filename cannot be empty!")
                continue
            try:
                self.conn = sqlite3.connect(db_file)
                self.cur = self.conn.cursor()
                print(f"✅ Connected to {db_file}")
                break
            except sqlite3.Error as e:
                print(f"❌ Error: {e}")
                return False
        return True

    def create_table(self):
        """Create a new table with custom columns"""
        if not self.conn:
            print("⚠️ Please connect to a database first!")
            return
        
        print("\n✨ Create New Table")
        while True:
            table_name = input("Table name (e.g., 'students'): ").strip()
            if table_name:
                break
            print("⚠️ Table name cannot be empty!")
        
        columns = []
        print("\nAdd columns (press Enter alone to finish):")
        while True:
            print(f"\nCurrent columns for '{table_name}':")
            for i, col in enumerate(columns, 1):
                print(f"{i}. {col}")
            
            print("\nAdd new column:")
            try:
                col_name = input("  Column name: ").strip()
                if not col_name:
                    if not columns:
                        print("⚠️ Table must have at least one column!")
                        continue
                    break
                
                print("  Common data types: INTEGER, TEXT, REAL, BLOB")
                while True:
                    col_type = input("  Data type: ").upper().strip()
                    if col_type in ('INTEGER', 'TEXT', 'REAL', 'BLOB'):
                        break
                    print("⚠️ Invalid type. Please use INTEGER, TEXT, REAL, or BLOB")
                
                constraints = []
                print("\n  Add constraints:")
                if input("    PRIMARY KEY? (y/n): ").lower() == 'y':
                    constraints.append("PRIMARY KEY")
                if input("    NOT NULL? (y/n): ").lower() == 'y':
                    constraints.append("NOT NULL")
                if input("    UNIQUE? (y/n): ").lower() == 'y':
                    constraints.append("UNIQUE")
                
                column_def = f"{col_name} {col_type}"
                if constraints:
                    column_def += " " + " ".join(constraints)
                
                columns.append(column_def)
            except KeyboardInterrupt:
                print("\n⚠️ Column addition cancelled")
                if input("Finish table creation? (y/n): ").lower() == 'y':
                    break
                continue
        
        # Add foreign keys
        fks = []
        print("\nAdd foreign keys (press Enter alone to skip):")
        while True:
            print("\nCurrent foreign keys:")
            for i, fk in enumerate(fks, 1):
                print(f"{i}. {fk}")
            
            print("\nAdd new foreign key:")
            try:
                fk_col = input("  Column name: ").strip()
                if not fk_col:
                    break
                
                ref_table = input("  References table: ").strip()
                ref_col = input("  References column: ").strip()
                
                fks.append(f"FOREIGN KEY({fk_col}) REFERENCES {ref_table}({ref_col})")
            except KeyboardInterrupt:
                print("\n⚠️ Foreign key addition cancelled")
                if input("Finish table creation? (y/n): ").lower() == 'y':
                    break
                continue
        
        # Build CREATE TABLE statement
        create_sql = f"CREATE TABLE {table_name} (\n  "
        create_sql += ",\n  ".join(columns + fks)
        create_sql += "\n);"
        
        print(f"\nSQL to be executed:\n{create_sql}")
        
        confirm = input("\nCreate this table? (y/n): ").lower()
        if confirm == 'y':
            try:
                self.cur.execute(create_sql)
                self.conn.commit()
                print(f"✅ Table '{table_name}' created successfully!")
            except sqlite3.Error as e:
                print(f"❌ Error creating table: {e}")
        else:
            print("🚫 Table creation cancelled.")

    def list_tables(self):
        """List all tables in the database"""
        if not self.conn:
            print("⚠️ Please connect to a database first!")
            return []
        
        self.cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [table[0] for table in self.cur.fetchall()]
        
        if tables:
            print("\n📋 Tables in database:")
            for i, table in enumerate(tables, 1):
                print(f"{i}. {table}")
        else:
            print("ℹ️ No tables found in database.")
        
        return tables

    def view_table(self, table_name=None):
        """View contents of a table"""
        if not self.conn:
            print("⚠️ Please connect to a database first!")
            return
        
        if not table_name:
            tables = self.list_tables()
            if not tables:
                return
            
            try:
                choice = int(input("\nEnter table number to view: ")) - 1
                table_name = tables[choice]
            except (ValueError, IndexError):
                print("❌ Invalid selection")
                return
        
        try:
            # Get table data
            self.cur.execute(f"SELECT * FROM {table_name}")
            data = self.cur.fetchall()
            
            # Get column names
            self.cur.execute(f"PRAGMA table_info({table_name})")
            headers = [col[1] for col in self.cur.fetchall()]
            
            if data:
                print(f"\n📊 Contents of '{table_name}':")
                print(tabulate(data, headers=headers, tablefmt="grid"))
            else:
                print(f"ℹ️ Table '{table_name}' is empty")
        except sqlite3.Error as e:
            print(f"❌ Error: {e}")

    def add_row(self):
        """Add a new row to a table"""
        tables = self.list_tables()
        if not tables:
            return
        
        try:
            choice = int(input("\nEnter table number to add to: ")) - 1
            table_name = tables[choice]
        except (ValueError, IndexError):
            print("❌ Invalid selection")
            return
        
        # Get column info
        self.cur.execute(f"PRAGMA table_info({table_name})")
        columns = self.cur.fetchall()
        
        print(f"\n➕ Add row to '{table_name}':")
        values = []
        for col in columns:
            col_name, col_type = col[1], col[2]
            constraints = []
            if col[3]: constraints.append("NOT NULL")
            if col[5]: constraints.append("PRIMARY KEY")
            
            prompt = f"  {col_name} ({col_type})"
            if constraints:
                prompt += f" [{' '.join(constraints)}]"
            prompt += ": "
            
            while True:
                value = input(prompt).strip()
                
                # Handle NULL values
                if not value:
                    if "NOT NULL" in constraints:
                        print("⚠️ This column cannot be NULL!")
                        continue
                    value = None
                    break
                
                # Type conversion
                try:
                    if col_type.upper() == "INTEGER":
                        value = int(value)
                    elif col_type.upper() == "REAL":
                        value = float(value)
                    break
                except ValueError:
                    print(f"⚠️ Invalid {col_type} value")
            
            values.append(value)
        
        # Build INSERT statement
        col_names = [col[1] for col in columns]
        placeholders = ",".join(["?"] * len(col_names))
        
        try:
            self.cur.execute(
                f"INSERT INTO {table_name} ({','.join(col_names)}) VALUES ({placeholders})",
                values
            )
            self.conn.commit()
            print("✅ Row added successfully!")
        except sqlite3.Error as e:
            print(f"❌ Error: {e}")

    def delete_row(self):
        """Delete a row from a table"""
        tables = self.list_tables()
        if not tables:
            return
        
        try:
            choice = int(input("\nEnter table number to delete from: ")) - 1
            table_name = tables[choice]
        except (ValueError, IndexError):
            print("❌ Invalid selection")
            return
        
        # Show table contents first
        self.view_table(table_name)
        
        # Get primary key
        self.cur.execute(f"PRAGMA table_info({table_name})")
        pk_col = next((col[1] for col in self.cur.fetchall() if col[5] > 0), None)
        
        if not pk_col:
            print("❌ No primary key found - cannot safely delete rows")
            return
        
        # Get row to delete
        row_id = input(f"\nEnter {pk_col} of row to delete: ").strip()
        
        # Verify row exists
        self.cur.execute(f"SELECT * FROM {table_name} WHERE {pk_col}=?", (row_id,))
        if not self.cur.fetchone():
            print("❌ Row not found!")
            return
        
        # Confirm deletion
        confirm = input(f"⚠️ Delete row with {pk_col}={row_id}? (y/n): ").lower()
        if confirm != 'y':
            print("🚫 Deletion cancelled")
            return
        
        # Execute deletion
        try:
            self.cur.execute(f"DELETE FROM {table_name} WHERE {pk_col}=?", (row_id,))
            self.conn.commit()
            print("✅ Row deleted successfully!")
        except sqlite3.Error as e:
            print(f"❌ Error: {e}")

    def close(self):
        """Close the database connection"""
        if self.conn:
            self.conn.close()
            print("🔌 Database connection closed")
        self.conn = None
        self.cur = None

def main():
    editor = DatabaseEditor()
    
    try:
        while True:
            print("\n" + "="*40)
            print("📝 SQLite Database Editor".center(40))
            print("="*40)
            print("1. Connect to/Create Database")
            print("2. Create Table")
            print("3. List Tables")
            print("4. View Table Data")
            print("5. Add Row")
            print("6. Delete Row")
            print("7. Exit")
            print("="*40)
            
            try:
                choice = input("\nSelect an option (1-7): ")
                
                if choice == "1":
                    editor.connect()
                elif choice == "2":
                    editor.create_table()
                elif choice == "3":
                    editor.list_tables()
                elif choice == "4":
                    editor.view_table()
                elif choice == "5":
                    editor.add_row()
                elif choice == "6":
                    editor.delete_row()
                elif choice == "7":
                    editor.close()
                    print("\n👋 Goodbye!")
                    break
                else:
                    print("❌ Invalid choice - please try again")
            except KeyboardInterrupt:
                print("\n⚠️ Operation cancelled")
                continue
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
    finally:
        if hasattr(editor, 'close'):
            editor.close()

if __name__ == "__main__":
    main()