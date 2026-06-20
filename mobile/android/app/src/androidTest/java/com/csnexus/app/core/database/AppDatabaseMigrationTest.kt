package com.csnexus.app.core.database

import android.database.sqlite.SQLiteDatabase
import androidx.room.Room
import androidx.sqlite.db.SupportSQLiteDatabase
import androidx.test.ext.junit.runners.AndroidJUnit4
import androidx.test.platform.app.InstrumentationRegistry
import org.junit.Assert.assertTrue
import org.junit.Test
import org.junit.runner.RunWith

@RunWith(AndroidJUnit4::class)
class AppDatabaseMigrationTest {
    @Test
    fun migrate1To2AddsOfflineSyncColumnsAndFlashcardCache() {
        val context = InstrumentationRegistry.getInstrumentation().targetContext
        context.deleteDatabase(TEST_DB)
        val path = context.getDatabasePath(TEST_DB).absolutePath
        SQLiteDatabase.openOrCreateDatabase(path, null).use { raw ->
            createVersionOneSchema(raw)
            raw.version = 1
        }

        val roomDatabase = Room.databaseBuilder(context, AppDatabase::class.java, TEST_DB)
            .addMigrations(AppDatabase.MIGRATION_1_2)
            .build()
        val migrated = roomDatabase.openHelper.writableDatabase

        assertTrue(hasColumn(migrated, "content_cache", "schemaVersion"))
        assertTrue(hasColumn(migrated, "lesson_cache", "schemaVersion"))
        assertTrue(hasTable(migrated, "flashcard_cache"))
        assertTrue(hasColumn(migrated, "sync_events", "payloadHash"))
        assertTrue(hasColumn(migrated, "sync_events", "idempotencyKey"))
        assertTrue(hasColumn(migrated, "sync_events", "updatedAtMillis"))
        assertTrue(hasColumn(migrated, "sync_events", "requiresAuth"))

        migrated.close()
        roomDatabase.close()
    }

    private fun createVersionOneSchema(database: SQLiteDatabase) {
        database.execSQL(
            """
            CREATE TABLE IF NOT EXISTS `content_cache` (
                `cacheKey` TEXT NOT NULL,
                `payloadJson` TEXT NOT NULL,
                `cachedAtMillis` INTEGER NOT NULL,
                PRIMARY KEY(`cacheKey`)
            )
            """.trimIndent(),
        )
        database.execSQL(
            """
            CREATE TABLE IF NOT EXISTS `lesson_cache` (
                `subtopicId` INTEGER NOT NULL,
                `payloadJson` TEXT NOT NULL,
                `cachedAtMillis` INTEGER NOT NULL,
                PRIMARY KEY(`subtopicId`)
            )
            """.trimIndent(),
        )
        database.execSQL(
            """
            CREATE TABLE IF NOT EXISTS `progress_snapshots` (
                `snapshotKey` TEXT NOT NULL,
                `payloadJson` TEXT NOT NULL,
                `cachedAtMillis` INTEGER NOT NULL,
                PRIMARY KEY(`snapshotKey`)
            )
            """.trimIndent(),
        )
        database.execSQL(
            """
            CREATE TABLE IF NOT EXISTS `finalized_reviews` (
                `reviewType` TEXT NOT NULL,
                `reviewId` TEXT NOT NULL,
                `payloadJson` TEXT NOT NULL,
                `cachedAtMillis` INTEGER NOT NULL,
                PRIMARY KEY(`reviewType`, `reviewId`)
            )
            """.trimIndent(),
        )
        database.execSQL(
            """
            CREATE TABLE IF NOT EXISTS `sync_events` (
                `id` TEXT NOT NULL,
                `feature` TEXT NOT NULL,
                `eventType` TEXT NOT NULL,
                `endpoint` TEXT NOT NULL,
                `payloadJson` TEXT NOT NULL,
                `status` TEXT NOT NULL,
                `attemptCount` INTEGER NOT NULL,
                `lastError` TEXT,
                `createdAtMillis` INTEGER NOT NULL,
                `lastAttemptAtMillis` INTEGER,
                PRIMARY KEY(`id`)
            )
            """.trimIndent(),
        )
    }

    private fun hasTable(database: SupportSQLiteDatabase, tableName: String): Boolean {
        database.query(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
            arrayOf(tableName),
        ).use { cursor ->
            return cursor.moveToFirst()
        }
    }

    private fun hasColumn(database: SupportSQLiteDatabase, tableName: String, columnName: String): Boolean {
        database.query("PRAGMA table_info(`$tableName`)").use { cursor ->
            val nameIndex = cursor.getColumnIndex("name")
            while (cursor.moveToNext()) {
                if (cursor.getString(nameIndex) == columnName) {
                    return true
                }
            }
        }
        return false
    }

    private companion object {
        const val TEST_DB = "migration-test.db"
    }
}
