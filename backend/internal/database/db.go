package database

import (
	"log"

	"github.com/jmoiron/sqlx"
	_ "github.com/lib/pq"
	"github.com/oliviarves/stock-tracker/internal/config"
)

// DB is our database connection
var DB *sqlx.DB

// Initialize sets up the database connection
func Initialize(config *config.Config) error {
	var err error

	// Connect to database
	DB, err = sqlx.Connect("postgres", config.DatabaseURL)
	if err != nil {
		return err
	}

	// Test the connection
	err = DB.Ping()
	if err != nil {
		return err
	}

	log.Println("Database connected successfully")

	// Run migrations
	err = migrateDatabase()
	if err != nil {
		return err
	}

	return nil
}

// migrateDatabase runs the necessary database migrations
func migrateDatabase() error {
	// For a simple approach, we'll create tables directly
	// In a production app, you might use a migration tool
	schema := `
	CREATE TABLE IF NOT EXISTS stocks (
		id SERIAL PRIMARY KEY,
		symbol TEXT NOT NULL,
		notes TEXT,
		watchlist BOOLEAN DEFAULT false,
		created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
		updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
	);

	CREATE TABLE IF NOT EXISTS tags (
		id SERIAL PRIMARY KEY,
		name TEXT UNIQUE NOT NULL,
		created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
	);

	CREATE TABLE IF NOT EXISTS stock_tags (
		stock_id INT REFERENCES stocks(id) ON DELETE CASCADE,
		tag_id INT REFERENCES tags(id) ON DELETE CASCADE,
		PRIMARY KEY (stock_id, tag_id)
	);
	`

	_, err := DB.Exec(schema)
	if err != nil {
		return err
	}

	log.Println("Database migration completed successfully")
	return nil
}

// Close closes the database connection
func Close() {
	if DB != nil {
		DB.Close()
	}
}
