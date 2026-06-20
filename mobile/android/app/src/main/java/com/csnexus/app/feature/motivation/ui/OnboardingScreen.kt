package com.csnexus.app.feature.motivation.ui

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.widthIn
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import com.csnexus.app.core.design.CSNexusButton
import com.csnexus.app.core.design.CSNexusButtonVariant
import com.csnexus.app.core.design.CSNexusChip
import com.csnexus.app.core.design.CSNexusTabs
import com.csnexus.app.core.design.CSNexusTextField
import com.csnexus.app.core.design.GlassMedium
import com.csnexus.app.core.design.MetallicText
import com.csnexus.app.core.error.userMessage
import com.csnexus.app.core.network.ApiResult
import com.csnexus.app.feature.motivation.data.MotivationRepository
import com.csnexus.app.feature.motivation.data.OnboardingDraft
import com.csnexus.app.feature.motivation.data.OnboardingExamCategory
import com.csnexus.app.feature.motivation.data.OnboardingRequestDto
import com.csnexus.app.feature.motivation.data.PlanSummaryDto
import kotlinx.coroutines.launch

@Composable
fun OnboardingScreen(
    repository: MotivationRepository,
    contentPadding: PaddingValues,
    onCompleted: () -> Unit,
    onSkipped: () -> Unit,
) {
    val scope = rememberCoroutineScope()
    val savedDraft = remember { repository.onboardingDraft() }
    var examDate by remember(savedDraft) { mutableStateOf(savedDraft?.examDate.orEmpty()) }
    var examCategory by remember(savedDraft) { mutableStateOf(savedDraft?.examCategory ?: OnboardingExamCategory.Professional) }
    var timeBudget by remember(savedDraft) { mutableIntStateOf(savedDraft?.timeBudgetMinutes ?: 30) }
    var selectedStep by remember(savedDraft) { mutableIntStateOf(savedDraft?.currentStep ?: 0) }
    var validationResult by remember(examDate) { mutableStateOf(repository.validateOnboardingDate(examDate)) }
    var loading by remember { mutableStateOf(false) }
    var errorMessage by remember { mutableStateOf<String?>(null) }
    var statusMessage by remember { mutableStateOf<String?>(null) }
    var planSummary by remember { mutableStateOf<PlanSummaryDto?>(null) }
    var planSummaryLoading by remember { mutableStateOf(false) }

    LaunchedEffect(examDate, examCategory, timeBudget, selectedStep) {
        repository.saveOnboardingDraft(
            OnboardingDraft(
                examDate = examDate,
                examCategory = examCategory,
                timeBudgetMinutes = timeBudget,
                currentStep = selectedStep,
            ),
        )
        validationResult = repository.validateOnboardingDate(examDate)
    }

    LaunchedEffect(selectedStep, examDate) {
        if (selectedStep == 2 && validationResult.errorMessage == null) {
            planSummaryLoading = true
            when (val result = repository.onboardingPlanSummary()) {
                is ApiResult.Success -> planSummary = result.value
                is ApiResult.Failure -> errorMessage = result.error.userMessage()
            }
            planSummaryLoading = false
        }
    }

    fun goNext() {
        if (selectedStep == 0 && validationResult.errorMessage != null) {
            errorMessage = validationResult.errorMessage
            return
        }
        errorMessage = null
        selectedStep = minOf(selectedStep + 1, onboardingStepLabels().lastIndex)
    }

    fun goBack() {
        selectedStep = maxOf(selectedStep - 1, 0)
    }

    fun submit() {
        if (validationResult.errorMessage != null) {
            errorMessage = validationResult.errorMessage
            return
        }
        loading = true
        errorMessage = null
        statusMessage = null
        scope.launch {
            when (
                val result = repository.submitOnboarding(
                    OnboardingRequestDto(
                        examDate = examDate,
                        examCategory = examCategory,
                        timeBudgetMinutes = timeBudget,
                    ),
                )
            ) {
                is ApiResult.Success -> {
                    repository.clearOnboardingDraft()
                    statusMessage = result.value.warning ?: result.value.confirmation
                    onCompleted()
                }
                is ApiResult.Failure -> errorMessage = result.error.userMessage()
            }
            loading = false
        }
    }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(contentPadding)
            .verticalScroll(rememberScrollState())
            .padding(20.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.spacedBy(14.dp),
    ) {
        Column(
            modifier = Modifier.widthIn(max = 520.dp).fillMaxWidth(),
            verticalArrangement = Arrangement.spacedBy(14.dp),
        ) {
        MetallicText("Set up your study plan", style = MaterialTheme.typography.headlineLarge)
        Text(
            "Tell the native app about your exam so we can keep planning, queueing, and milestones aligned.",
            color = MaterialTheme.colorScheme.onSurfaceVariant,
        )

        CSNexusTabs(
            tabs = onboardingStepLabels(),
            selectedIndex = selectedStep,
            onSelected = { index ->
                if (index <= selectedStep || validationResult.errorMessage == null) {
                    selectedStep = index
                }
            },
        )

        when (selectedStep) {
            0 -> OnboardingDateStep(
                examDate = examDate,
                onExamDateChange = { examDate = it },
                validationResult = validationResult,
            )
            1 -> OnboardingCategoryStep(
                examCategory = examCategory,
                onExamCategoryChange = { examCategory = it },
            )
            else -> OnboardingTimeBudgetStep(
                timeBudget = timeBudget,
                onTimeBudgetChange = { timeBudget = it },
                planSummary = planSummary,
                loading = planSummaryLoading,
            )
        }

        if (errorMessage != null) {
            Text(errorMessage!!, color = MaterialTheme.colorScheme.error)
        }
        if (statusMessage != null) {
            Text(statusMessage!!, color = MaterialTheme.colorScheme.primary)
        }

        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.spacedBy(10.dp),
        ) {
            CSNexusButton(
                text = "Skip for now",
                onClick = {
                    repository.markOnboardingSkipped(true)
                    repository.clearOnboardingDraft()
                    onSkipped()
                },
                variant = CSNexusButtonVariant.Ghost,
                modifier = Modifier.weight(1f),
                enabled = !loading,
            )
            if (selectedStep > 0) {
                CSNexusButton(
                    text = "Back",
                    onClick = ::goBack,
                    variant = CSNexusButtonVariant.Secondary,
                    modifier = Modifier.weight(1f),
                    enabled = !loading,
                )
            }
            CSNexusButton(
                text = if (selectedStep == onboardingStepLabels().lastIndex) {
                    if (loading) "Creating..." else "Create My Plan"
                } else {
                    "Continue"
                },
                onClick = if (selectedStep == onboardingStepLabels().lastIndex) ::submit else ::goNext,
                loading = loading,
                modifier = Modifier.weight(1f),
            )
        }
        } // end widthIn column
    }
}

@Composable
private fun OnboardingDateStep(
    examDate: String,
    onExamDateChange: (String) -> Unit,
    validationResult: OnboardingValidationResult,
) {
    GlassMedium(modifier = Modifier.fillMaxWidth()) {
        Column(modifier = Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(10.dp)) {
            Text("Exam date", style = MaterialTheme.typography.titleMedium)
            CSNexusTextField(
                value = examDate,
                onValueChange = onExamDateChange,
                label = "YYYY-MM-DD",
                supportingText = "Must be 1-365 days from today",
                isError = validationResult.errorMessage != null,
            )
            validationResult.warningMessage?.let {
                Text(it, color = MaterialTheme.colorScheme.primary, fontWeight = FontWeight.SemiBold)
            }
        }
    }
}

@Composable
private fun OnboardingCategoryStep(
    examCategory: OnboardingExamCategory,
    onExamCategoryChange: (OnboardingExamCategory) -> Unit,
) {
    GlassMedium(modifier = Modifier.fillMaxWidth()) {
        Column(modifier = Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(10.dp)) {
            Text("Exam category", style = MaterialTheme.typography.titleMedium)
            Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                onboardingExamCategoryOptions().forEach { option ->
                    CSNexusChip(
                        text = option.label,
                        selected = examCategory == option,
                        onClick = { onExamCategoryChange(option) },
                    )
                }
            }
        }
    }
}

@Composable
private fun OnboardingTimeBudgetStep(
    timeBudget: Int,
    onTimeBudgetChange: (Int) -> Unit,
    planSummary: PlanSummaryDto?,
    loading: Boolean,
) {
    Column(verticalArrangement = Arrangement.spacedBy(14.dp)) {
        GlassMedium(modifier = Modifier.fillMaxWidth()) {
            Column(modifier = Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(10.dp)) {
                Text("Daily study time", style = MaterialTheme.typography.titleMedium)
                Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    onboardingTimeBudgets().forEach { minutes ->
                        CSNexusChip(
                            text = "$minutes min",
                            selected = timeBudget == minutes,
                            onClick = { onTimeBudgetChange(minutes) },
                        )
                    }
                }
            }
        }
        GlassMedium(modifier = Modifier.fillMaxWidth()) {
            Column(modifier = Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                Text("Plan preview", style = MaterialTheme.typography.titleMedium)
                if (loading) {
                    Text("Loading plan summary...", color = MaterialTheme.colorScheme.onSurfaceVariant)
                } else if (planSummary == null) {
                    Text("Plan details will appear after the server computes them.", color = MaterialTheme.colorScheme.onSurfaceVariant)
                } else {
                    Text("${planSummary.totalDays} total study days")
                    Text("${planSummary.subtopicsPerWeek} subtopics per week")
                    Text("${planSummary.mockExamsScheduled} mock exams scheduled")
                    Text("${planSummary.estimatedReadinessAtExam}% estimated readiness by exam day")
                }
            }
        }
    }
}
