package models

import (
	"time"

	"github.com/jmoiron/sqlx"
	"github.com/yourusername/stock-tracker/internal/database"
)

type Tag struct {
	ID        int       `db:"id" json:"id"`
	Name      string    `db:"name" json:"name"`
	CreatedAt time.Time `db:"created_at" json:"created_at"`
}

// GetTags returns all tags
func GetTags() ([]Tag, error) {
	var tags []Tag
	err := database.DB.Select(&tags, "SELECT * FROM tags ORDER BY name")
	return tags, err
}

// GetTagsByStockID returns all tags for a stock
func GetTagsByStockID(stockID int) ([]Tag, error) {
	var tags []Tag

	query := `
		SELECT t.* FROM tags t
		JOIN stock_tags st ON t.id = st.tag_id
		WHERE st.stock_id = $1
		ORDER BY t.name
	`

	err := database.DB.Select(&tags, query, stockID)
	return tags, err
}

// getOrCreateTag gets an existing tag or creates a new one in a transaction
func getOrCreateTag(tx *sqlx.Tx, name string) (int, error) {
	var id int

	// Try to get existing tag
	err := tx.Get(&id, "SELECT id FROM tags WHERE name = $1", name)
	if err == nil {
		return id, nil
	}

	// Create new tag
	err = tx.QueryRowx(
		"INSERT INTO tags (name) VALUES ($1) RETURNING id",
		name,
	).Scan(&id)

	return id, err
}
