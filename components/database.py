import os
import pymysql
from sshtunnel import SSHTunnel
import paramiko
from typing import Optional, Tuple, Any

class RDSSSHConnector:
    def __init__(self):
        # SSH configuration
        self.ssh_host = os.environ['SSH_HOST']
        self.ssh_user = os.environ['SSH_USER']
        self.ssh_private_key = os.environ['SSH_PRIVATE_KEY_PATH']
        
        # Database configuration
        self.db_host = os.environ['DB_HOST']
        self.db_user = os.environ['DB_USER']
        self.db_password = os.environ['DB_PASSWORD']
        self.db_name = os.environ['DB_NAME']
        self.db_port = int(os.environ.get('DB_PORT', 3306))
        
        self.connection = None
        self.tunnel = None

    def __enter__(self):
        """Context manager entry point"""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit point"""
        self.close()

    def connect(self) -> None:
        """Establish SSH tunnel and database connection"""
        try:
            # Create SSH tunnel
            self.tunnel = SSHTunnel(
                self.ssh_host,
                ssh_username=self.ssh_user,
                ssh_pkey=self.ssh_private_key,
                remote_bind_address=(self.db_host, self.db_port)
            )
            
            self.tunnel.start()

            # Create database connection through the SSH tunnel
            self.connection = pymysql.connect(
                host='127.0.0.1',
                user=self.db_user,
                password=self.db_password,
                database=self.db_name,
                port=self.tunnel.local_bind_port,
                ssl={'ssl': True}
            )

        except Exception as e:
            self.close()
            raise Exception(f"Failed to establish connection: {str(e)}")

    def close(self) -> None:
        """Close all connections"""
        if self.connection:
            self.connection.close()
            self.connection = None
        if self.tunnel:
            self.tunnel.close()
            self.tunnel = None

    def execute_query(self, query: str, params: Optional[Tuple] = None) -> Any:
        """Execute a query and return results"""
        try:
            if not self.connection:
                self.connect()

            with self.connection.cursor() as cursor:
                cursor.execute(query, params)
                return cursor.fetchall()

        except Exception as e:
            raise Exception(f"Query execution failed: {str(e)}")

class DatabaseError(Exception):
    """Custom exception for database operations"""
    pass

# Example usage:
if __name__ == "__main__":
    try:
        # Using context manager (recommended)
        with RDSSSHConnector() as db:
            # Read query example
            select_query = "SELECT * FROM users WHERE active = %s LIMIT %s"
            results = db.execute_query(select_query, (True, 10))
            for row in results:
                print(row)

            # Write query example
            insert_query = "INSERT INTO users (name, email) VALUES (%s, %s)"
            db.execute_write_query(insert_query, ('John Doe', 'john@example.com'))

    except Exception as e:
        print(f"Error: {str(e)}")

    # Alternative usage without context manager
    """
    db = RDSSSHConnector()
    try:
        db.connect()
        results = db.execute_query("SELECT * FROM users LIMIT 10")
        for row in results:
            print(row)
    finally:
        db.close()
    """
