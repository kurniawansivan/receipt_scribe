import sqlite3
import json
import logging
from contextlib import contextmanager
from app.models.schemas import ExpenseCreate, ExpenseResponse
from typing import List, Iterator

logger = logging.getLogger(__name__)

class DatabaseService:
    def __init__(self, db_path: str = "receipts.db"):
        self.db_path = db_path
        self._init_db()

    @contextmanager
    def _get_connection(self) -> Iterator[sqlite3.Connection]:
        """Context manager for database connections"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Enable dict-like access
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def _init_db(self):
        """Initialize database with required tables"""
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vendor_name TEXT,
            date TEXT,
            total_amount REAL,
            tax_amount REAL,
            items_json TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        """
        try:
            with self._get_connection() as conn:
                conn.execute(create_table_sql)
            logger.info("Database initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing database: {str(e)}")
            raise

    def create_expense(self, expense: ExpenseCreate) -> int:
        """Create a new expense record"""
        items_json = json.dumps([item.dict() for item in expense.items]) if expense.items else "[]"
        
        insert_sql = """
        INSERT INTO expenses (vendor_name, date, total_amount, tax_amount, items_json)
        VALUES (?, ?, ?, ?, ?)
        """
        
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    insert_sql,
                    [
                        expense.vendor_name,
                        expense.date.isoformat() if expense.date else None,
                        expense.total_amount,
                        expense.tax_amount,
                        items_json
                    ]
                )
                return cursor.lastrowid
        except Exception as e:
            logger.error(f"Error creating expense: {str(e)}")
            raise

    def get_all_expenses(self) -> List[ExpenseResponse]:
        """Get all expenses ordered by date (newest first)"""
        select_sql = """
        SELECT id, vendor_name, date, total_amount, tax_amount, items_json
        FROM expenses 
        ORDER BY date DESC, created_at DESC
        """
        
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(select_sql)
                rows = cursor.fetchall()
                
                expenses = []
                for row in rows:
                    items = json.loads(row['items_json']) if row['items_json'] else []
                    expense = ExpenseResponse(
                        id=row['id'],
                        vendor_name=row['vendor_name'],
                        date=row['date'],
                        total_amount=row['total_amount'],
                        tax_amount=row['tax_amount'],
                        items=items
                    )
                    expenses.append(expense)
                return expenses
        except Exception as e:
            logger.error(f"Error getting expenses: {str(e)}")
            return []

    def get_expense_summary(self) -> dict:
        """Get summary statistics for dashboard"""
        summary_sql = """
        SELECT 
            COUNT(*) as expense_count,
            COALESCE(SUM(total_amount), 0) as total_amount,
            COALESCE(SUM(tax_amount), 0) as total_tax
        FROM expenses
        """
        
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(summary_sql)
                row = cursor.fetchone()
                
                return {
                    "expense_count": row['expense_count'] or 0,
                    "total_amount": row['total_amount'] or 0.0,
                    "total_tax": row['total_tax'] or 0.0
                }
        except Exception as e:
            logger.error(f"Error getting summary: {str(e)}")
            return {
                "expense_count": 0,
                "total_amount": 0.0,
                "total_tax": 0.0
            }

    def get_expenses_by_month(self) -> dict:
        """Get expenses grouped by month for charts"""
        monthly_sql = """
        SELECT 
            strftime('%Y-%m', date) as month,
            SUM(total_amount) as total
        FROM expenses 
        WHERE date IS NOT NULL
        GROUP BY strftime('%Y-%m', date)
        ORDER BY month
        """
        
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(monthly_sql)
                rows = cursor.fetchall()
                
                return {row['month']: row['total'] for row in rows}
        except Exception as e:
            logger.error(f"Error getting monthly data: {str(e)}")
            return {}

# Global instance - simple and effective
db_service = DatabaseService()