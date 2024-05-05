CREATE TABLE "users" (
    "id" INTEGER,
    "username" TEXT NOT NULL UNIQUE,
    "password" TEXT NOT NULL,
    "role" TEXT NOT NULL CHECK("role" IN ('free', 'premium', 'admin')) DEFAULT "free",
    "registration_datetime" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY("id")
);

CREATE TABLE "lists" (
    "id" INTEGER,
    "list_title" TEXT NOT NULL UNIQUE,
    PRIMARY KEY("id")
);

CREATE TABLE user_lists (
    "user_id" INTEGER,
    "list_id" INTEGER,
    FOREIGN KEY("user_id") REFERENCES "users"("id") ON DELETE CASCADE,
    FOREIGN KEY("list_id") REFERENCES "lists"("id") ON DELETE CASCADE
);

CREATE TABLE user_fav (
    "user_id" INTEGER,
    "movie_id" INTEGER,
    FOREIGN KEY("user_id") REFERENCES "users"("id") ON DELETE CASCADE
);

CREATE TABLE user_watched (
    "user_id" INTEGER,
    "movie_id" INTEGER,
    FOREIGN KEY("user_id") REFERENCES "users"("id") ON DELETE CASCADE
);

CREATE TABLE user_watch_list (
    "user_id" INTEGER,
    "movie_id" INTEGER,
    FOREIGN KEY("user_id") REFERENCES "users"("id") ON DELETE CASCADE
);