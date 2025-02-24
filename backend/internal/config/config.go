package config

import (
	"log"
	"os"

	"github.com/joho/godotenv"
)

// Config holds all configuration for our application
type Config struct {
	DatabaseURL  string
	Port         string
	JWTSecret    string
	AllowOrigins string
}

// Load returns a Config struct populated from environment variables
func Load() *Config {
	// Load .env file if it exists
	err := godotenv.Load()
	if err != nil {
		log.Println("No .env file found, using environment variables")
	}

	config := &Config{
		DatabaseURL:  getEnv("DATABASE_URL", "postgres://postgres:postgres@localhost:5432/stocktracker?sslmode=disable"),
		Port:         getEnv("PORT", "8080"),
		JWTSecret:    getEnv("JWT_SECRET", "your-secret-key"),
		AllowOrigins: getEnv("ALLOW_ORIGINS", "http://localhost:3000"),
	}

	return config
}

// Helper function to get environment variable with a default value
func getEnv(key, defaultValue string) string {
	value := os.Getenv(key)
	if value == "" {
		return defaultValue
	}
	return value
}
