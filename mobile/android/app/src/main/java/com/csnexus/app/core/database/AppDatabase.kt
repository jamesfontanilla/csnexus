package com.csnexus.app.core.database

import android.content.Context
import androidx.room.Dao
import androidx.room.Database
import androidx.room.Entity
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.PrimaryKey
import androidx.room.Query
import androidx.room.Room
import androidx.room.RoomDatabase
import androidx.room.migration.Migration
import androidx.sqlite.db.SupportSQLiteDatabase
import kotlinx.coroutines.flow.Flow

object DatabaseContract {
    const val DATABASE_NAME = "csnexus.db"
    const val VERSION = 2
}

@Entity(tableName = "content_cache")
data class ContentCacheEntity(
    @PrimaryKey val cacheKey: String,
    val payloadJson: String,
    val cachedAtMillis: Long,
    val schemaVersion: Int = 1,
)

@Entity(tableName = "lesson_cache")
data class LessonCacheEntity(
    @PrimaryKey val subtopicId: Int,
    val payloadJson: String,
    val cachedAtMillis: Long,
    val schemaVersion: Int = 1,
)

@Entity(tableName = "flashcard_cache")
data class FlashcardCacheEntity(
    @PrimaryKey val cacheKey: String,
    val payloadJson: String,
    val cachedAtMillis: Long,
    val schemaVersion: Int = 1,
)

@Entity(tableName = "progress_snapshots")
data class ProgressSnapshotEntity(
    @PrimaryKey val snapshotKey: String,
    val payloadJson: String,
    val cachedAtMillis: Long,
)

@Entity(tableName = "finalized_reviews", primaryKeys = ["reviewType", "reviewId"])
data class FinalizedReviewEntity(
    val reviewType: String,
    val reviewId: String,
    val payloadJson: String,
    val cachedAtMillis: Long,
)

@Entity(tableName = "sync_events")
data class SyncEventEntity(
    @PrimaryKey val id: String,
    val feature: String,
    val eventType: String,
    val endpoint: String,
    val payloadJson: String,
    val payloadHash: String,
    val idempotencyKey: String,
    val status: String,
    val attemptCount: Int,
    val lastError: String? = null,
    val createdAtMillis: Long,
    val updatedAtMillis: Long,
    val lastAttemptAtMillis: Long? = null,
    val requiresAuth: Boolean = true,
)

@Dao
interface ContentCacheDao {
    @Query("SELECT * FROM content_cache WHERE cacheKey = :cacheKey")
    suspend fun get(cacheKey: String): ContentCacheEntity?

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun put(entity: ContentCacheEntity)

    @Query("DELETE FROM content_cache WHERE cacheKey = :cacheKey")
    suspend fun delete(cacheKey: String)
}

@Dao
interface LessonCacheDao {
    @Query("SELECT * FROM lesson_cache WHERE subtopicId = :subtopicId")
    suspend fun get(subtopicId: Int): LessonCacheEntity?

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun put(entity: LessonCacheEntity)
}

@Dao
interface FlashcardCacheDao {
    @Query("SELECT * FROM flashcard_cache WHERE cacheKey = :cacheKey")
    suspend fun get(cacheKey: String): FlashcardCacheEntity?

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun put(entity: FlashcardCacheEntity)
}

@Dao
interface ProgressSnapshotDao {
    @Query("SELECT * FROM progress_snapshots WHERE snapshotKey = :snapshotKey")
    suspend fun get(snapshotKey: String): ProgressSnapshotEntity?

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun put(entity: ProgressSnapshotEntity)
}

@Dao
interface FinalizedReviewDao {
    @Query("SELECT * FROM finalized_reviews WHERE reviewType = :reviewType AND reviewId = :reviewId")
    suspend fun get(reviewType: String, reviewId: String): FinalizedReviewEntity?

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun put(entity: FinalizedReviewEntity)
}

@Dao
interface SyncEventDao {
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun upsert(entity: SyncEventEntity)

    @Query("SELECT * FROM sync_events WHERE id = :id")
    suspend fun get(id: String): SyncEventEntity?

    @Query("SELECT * FROM sync_events WHERE status IN ('queued', 'failed') ORDER BY createdAtMillis ASC")
    suspend fun pending(): List<SyncEventEntity>

    @Query("SELECT * FROM sync_events WHERE feature = :feature AND status IN ('queued', 'syncing', 'failed', 'conflict') ORDER BY updatedAtMillis DESC")
    fun observeFeature(feature: String): Flow<List<SyncEventEntity>>

    @Query("SELECT * FROM sync_events WHERE feature = :feature AND status IN ('queued', 'failed') ORDER BY createdAtMillis ASC")
    suspend fun pendingByFeature(feature: String): List<SyncEventEntity>

    @Query("DELETE FROM sync_events WHERE id = :id")
    suspend fun delete(id: String)

    @Query("DELETE FROM sync_events WHERE status = 'synced'")
    suspend fun deleteSynced()
}

@Database(
    entities = [
        ContentCacheEntity::class,
        LessonCacheEntity::class,
        FlashcardCacheEntity::class,
        ProgressSnapshotEntity::class,
        FinalizedReviewEntity::class,
        SyncEventEntity::class,
    ],
    version = DatabaseContract.VERSION,
    exportSchema = false,
)
abstract class AppDatabase : RoomDatabase() {
    abstract fun contentCacheDao(): ContentCacheDao
    abstract fun lessonCacheDao(): LessonCacheDao
    abstract fun flashcardCacheDao(): FlashcardCacheDao
    abstract fun progressSnapshotDao(): ProgressSnapshotDao
    abstract fun finalizedReviewDao(): FinalizedReviewDao
    abstract fun syncEventDao(): SyncEventDao

    companion object {
        val MIGRATION_1_2 = object : Migration(1, 2) {
            override fun migrate(database: SupportSQLiteDatabase) {
                database.execSQL("ALTER TABLE content_cache ADD COLUMN schemaVersion INTEGER NOT NULL DEFAULT 1")
                database.execSQL("ALTER TABLE lesson_cache ADD COLUMN schemaVersion INTEGER NOT NULL DEFAULT 1")
                database.execSQL(
                    """
                    CREATE TABLE IF NOT EXISTS `flashcard_cache` (
                        `cacheKey` TEXT NOT NULL,
                        `payloadJson` TEXT NOT NULL,
                        `cachedAtMillis` INTEGER NOT NULL,
                        `schemaVersion` INTEGER NOT NULL DEFAULT 1,
                        PRIMARY KEY(`cacheKey`)
                    )
                    """.trimIndent(),
                )
                database.execSQL("ALTER TABLE sync_events ADD COLUMN payloadHash TEXT NOT NULL DEFAULT ''")
                database.execSQL("ALTER TABLE sync_events ADD COLUMN idempotencyKey TEXT NOT NULL DEFAULT ''")
                database.execSQL("ALTER TABLE sync_events ADD COLUMN updatedAtMillis INTEGER NOT NULL DEFAULT 0")
                database.execSQL("ALTER TABLE sync_events ADD COLUMN requiresAuth INTEGER NOT NULL DEFAULT 1")
                database.execSQL("UPDATE sync_events SET updatedAtMillis = createdAtMillis")
                database.execSQL("UPDATE sync_events SET payloadHash = id")
                database.execSQL("UPDATE sync_events SET idempotencyKey = id")
            }
        }

        @Volatile
        private var instance: AppDatabase? = null

        fun get(context: Context): AppDatabase {
            return instance ?: synchronized(this) {
                instance ?: Room.databaseBuilder(
                    context.applicationContext,
                    AppDatabase::class.java,
                    DatabaseContract.DATABASE_NAME,
                )
                    .addMigrations(MIGRATION_1_2)
                    .build()
                    .also { instance = it }
            }
        }
    }
}
