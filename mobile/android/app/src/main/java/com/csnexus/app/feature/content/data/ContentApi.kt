package com.csnexus.app.feature.content.data

import retrofit2.http.GET
import retrofit2.http.Header
import retrofit2.http.Path
import retrofit2.http.POST
import retrofit2.http.Body

interface ContentApi {
    @GET("v1/modules")
    suspend fun modules(): PaginatedResponseDto<ModuleDto>

    @GET("v1/modules/{moduleId}/topics")
    suspend fun topics(@Path("moduleId") moduleId: Int): List<TopicDto>

    @GET("v1/topics/{topicId}/subtopics")
    suspend fun subtopics(@Path("topicId") topicId: Int): List<SubtopicDto>

    @GET("v1/subtopics/{subtopicId}/lesson")
    suspend fun lesson(@Path("subtopicId") subtopicId: Int): LessonDto

    @POST("v1/subtopics/{subtopicId}/lesson:complete")
    suspend fun completeLesson(
        @Path("subtopicId") subtopicId: Int,
        @Body request: LessonCompleteRequestDto,
        @Header("Idempotency-Key") idempotencyKey: String? = null,
    ): LessonCompletionDto
}
