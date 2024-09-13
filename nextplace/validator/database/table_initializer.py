from nextplace.validator.database.database_manager import DatabaseManager

"""
Helper class to setup database tables, indices
"""


class TableInitializer:
    def __init__(self, database_manager: DatabaseManager):
        self.database_manager = database_manager

    def create_tables(self) -> None:
        """
        Create all validator tables
        Returns:
            None
        """
        cursor, db_connection = self.database_manager.get_cursor()
        self._create_properties_table(cursor)
        self._create_predictions_table(cursor)
        self._create_sales_table(cursor)
        self._create_miner_scores_table(cursor)
        db_connection.commit()
        cursor.close()
        db_connection.close()

    def _create_sales_table(self, cursor) -> None:
        """
        Create the sales table
        Args:
            cursor: a database cursor

        Returns:
            None
        """
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sales (
                property_id TEXT PRIMARY KEY,
                sale_price REAL,
                sale_date DATE
            )
        ''')
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_sale_date ON sales(sale_date)
        ''')

    def _create_predictions_table(self, cursor) -> None:
        """
        Create the predictions table
        Args:
            cursor: a database cursor

        Returns:
            None
        """
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS predictions (
                property_id TEXT,
                market TEXT,
                miner_hotkey TEXT,
                predicted_sale_price REAL,
                predicted_sale_date DATE,
                prediction_timestamp DATETIME,
                scored BOOLEAN,
                score_timestamp DATETIME,
                sent_to_site BOOLEAN,
                PRIMARY KEY (property_id, miner_hotkey)
                )
        ''')
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_prediction_timestamp ON predictions(prediction_timestamp)
        ''')
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_score_timestamp ON predictions(score_timestamp)
        ''')
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_scored ON predictions(scored)
        ''')
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_market ON predictions(market)
        ''')


    def _create_properties_table(self, cursor) -> None:
        """
        Create the properties table
        Args:
            cursor: a database cursor

        Returns:
            None
        """
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS properties (
                property_id TEXT PRIMARY KEY,
                listing_id TEXT,
                address TEXT,
                city TEXT,
                state TEXT,
                zip TEXT,
                price INTEGER,
                beds INTEGER,
                baths REAL,
                sqft INTEGER,
                lot_size INTEGER,
                year_built INTEGER,
                days_on_market INTEGER,
                latitude REAL,
                longitude REAL,
                property_type TEXT,
                last_sale_date TEXT,
                hoa_dues INTEGER,
                query_date TEXT,
                market TEXT
            )
        ''')


    def _create_miner_scores_table(self, cursor) -> None:
        """
        Create the miner scores table
        Args:
            cursor: a database cursor

        Returns:
            None
        """
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS miner_scores (
                miner_hotkey TEXT PRIMARY KEY,
                lifetime_score REAL,
                total_predictions INTEGER,
                last_update_timestamp DATETIME
            )
        ''')