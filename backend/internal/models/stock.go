package models

import (
	"time"

	"github.com/oliviarves/stock-tracker/internal/database"
)

type Stock struct {
	ID        int       `db:"id" json:"id"`
	Symbol    string    `db:"symbol" json:"symbol"`
	Notes     string    `db:"notes" json:"notes"`
	Watchlist bool      `db:"watchlist" json:"watchlist"`
	CreatedAt time.Time `db:"created_at" json:"created_at"`
	UpdatedAt time.Time `db:"updated_at" json:"updated_at"`
	Tags      []Tag     `json:"tags"`
}

// GetStocks returns all stocks with their tags
func GetStocks() ([]Stock, error) {
	var stocks []Stock

	// Get all stocks
	err := database.DB.Select(&stocks, "SELECT * FROM stocks ORDER BY symbol")
	if err != nil {
		return nil, err
	}

	// For each stock, get its tags
	for i := range stocks {
		tags, err := GetTagsByStockID(stocks[i].ID)
		if err != nil {
			return nil, err
		}
		stocks[i].Tags = tags
	}

	return stocks, nil
}

// GetStock returns a single stock by ID with its tags
func GetStock(id int) (Stock, error) {
	var stock Stock

	err := database.DB.Get(&stock, "SELECT * FROM stocks WHERE id = $1", id)
	if err != nil {
		return stock, err
	}

	// Get tags for this stock
	tags, err := GetTagsByStockID(stock.ID)
	if err != nil {
		return stock, err
	}
	stock.Tags = tags

	return stock, nil
}

// CreateStock creates a new stock with tags
func CreateStock(stock Stock, tagNames []string) (Stock, error) {
	tx, err := database.DB.Beginx()
	if err != nil {
		return stock, err
	}

	// Insert the stock
	query := `
		INSERT INTO stocks (symbol, notes, watchlist) 
		VALUES ($1, $2, $3)
		RETURNING id, created_at, updated_at
	`

	err = tx.QueryRowx(
		query,
		stock.Symbol,
		stock.Notes,
		stock.Watchlist,
	).Scan(&stock.ID, &stock.CreatedAt, &stock.UpdatedAt)

	if err != nil {
		tx.Rollback()
		return stock, err
	}

	// Handle tags
	for _, tagName := range tagNames {
		tagID, err := getOrCreateTag(tx, tagName)
		if err != nil {
			tx.Rollback()
			return stock, err
		}

		// Add relation
		_, err = tx.Exec(
			"INSERT INTO stock_tags (stock_id, tag_id) VALUES ($1, $2)",
			stock.ID, tagID,
		)

		if err != nil {
			tx.Rollback()
			return stock, err
		}
	}

	// Get tags to return
	tags, err := GetTagsByStockID(stock.ID)
	if err != nil {
		tx.Rollback()
		return stock, err
	}
	stock.Tags = tags

	err = tx.Commit()
	if err != nil {
		return stock, err
	}

	return stock, nil
}

// UpdateStock updates a stock and its tags
func UpdateStock(stock Stock, tagNames []string) (Stock, error) {
	tx, err := database.DB.Beginx()
	if err != nil {
		return stock, err
	}

	// Update the stock
	_, err = tx.Exec(
		"UPDATE stocks SET symbol = $1, notes = $2, watchlist = $3, updated_at = NOW() WHERE id = $4",
		stock.Symbol, stock.Notes, stock.Watchlist, stock.ID,
	)

	if err != nil {
		tx.Rollback()
		return stock, err
	}

	// Delete existing tag relationships
	_, err = tx.Exec("DELETE FROM stock_tags WHERE stock_id = $1", stock.ID)
	if err != nil {
		tx.Rollback()
		return stock, err
	}

	// Add new tags
	for _, tagName := range tagNames {
		tagID, err := getOrCreateTag(tx, tagName)
		if err != nil {
			tx.Rollback()
			return stock, err
		}

		// Add relation
		_, err = tx.Exec(
			"INSERT INTO stock_tags (stock_id, tag_id) VALUES ($1, $2)",
			stock.ID, tagID,
		)

		if err != nil {
			tx.Rollback()
			return stock, err
		}
	}

	// Get updated stock with tags
	err = tx.Get(&stock, "SELECT * FROM stocks WHERE id = $1", stock.ID)
	if err != nil {
		tx.Rollback()
		return stock, err
	}

	// Get tags to return
	tags, err := GetTagsByStockID(stock.ID)
	if err != nil {
		tx.Rollback()
		return stock, err
	}
	stock.Tags = tags

	err = tx.Commit()
	if err != nil {
		return stock, err
	}

	return stock, nil
}

// DeleteStock deletes a stock by ID
func DeleteStock(id int) error {
	_, err := database.DB.Exec("DELETE FROM stocks WHERE id = $1", id)
	return err
}
