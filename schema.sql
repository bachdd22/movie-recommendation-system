CREATE TABLE IF NOT EXISTS "users" (
    "id" INTEGER,
    "username" TEXT NOT NULL UNIQUE,
    "password" TEXT NOT NULL,
    "role" TEXT NOT NULL CHECK("role" IN ('free', 'premium', 'admin')) DEFAULT "free",
    "registration_datetime" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY("id")
);

CREATE TABLE "lists" (
    "id" INTEGER,
    "user_id" INTEGER,
    "list_title" TEXT NOT NULL,
    PRIMARY KEY("id"),
    FOREIGN KEY("user_id") REFERENCES "users"("id") ON DELETE CASCADE,
    UNIQUE(user_id, list_title)
);

