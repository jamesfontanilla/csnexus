package com.csnexus.app.feature.content.ui

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.widthIn
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.text.selection.SelectionContainer
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ExpandMore
import androidx.compose.material.icons.filled.ExpandLess
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.material3.Icon
import androidx.compose.runtime.Composable
import androidx.compose.runtime.mutableStateListOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.getValue
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.semantics.Role
import androidx.compose.ui.semantics.role
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import com.csnexus.app.core.design.CSNexusCard
import com.csnexus.app.core.design.CSNexusStatusBadge
import com.csnexus.app.feature.content.domain.LessonBlock
import kotlin.math.max

@Composable
fun LessonBlockRenderer(
    block: LessonBlock,
    modifier: Modifier = Modifier,
) {
    Column(modifier = modifier.fillMaxWidth()) {
        when (block.type) {
            "prose" -> ProseBlock(block.text)
            "table" -> TableBlock(block)
            "code" -> MonospaceBlock(block, label = block.language ?: "code")
            "formula" -> MonospaceBlock(block, label = block.language ?: "formula")
            "tip" -> CalloutBlock("Tip", block.text, MaterialTheme.colorScheme.primary)
            "warning" -> CalloutBlock("Watch out", block.text, MaterialTheme.colorScheme.error)
            "example" -> ExampleBlock(block.text)
            "step_by_step" -> StepBlock(block.items.ifEmpty { block.text.lines() })
            "list" -> ListBlock(block.items.ifEmpty { block.text.lines() })
            "svg", "image" -> MediaFallbackBlock(block)
            "check_understanding" -> CheckUnderstandingBlock(block)
            else -> UnknownBlock(block)
        }
    }
}

@Composable
private fun ProseBlock(text: String) {
    if (text.isBlank()) return
    Text(
        text = text,
        modifier = Modifier.padding(vertical = 8.dp),
        style = MaterialTheme.typography.bodyLarge,
    )
}

@Composable
private fun TableBlock(block: LessonBlock) {
    if (block.headers.isEmpty() && block.rows.isEmpty()) {
        UnknownBlock(block.copy(fallbackText = block.fallbackText ?: block.text.ifBlank { "Table data is unavailable." }))
        return
    }

    val columnCount = max(
        block.headers.size,
        block.rows.maxOfOrNull { it.size } ?: 0,
    )

    Column(
        modifier = Modifier
            .fillMaxWidth()
            .horizontalScroll(rememberScrollState())
            .padding(vertical = 12.dp),
    ) {
        Row(Modifier.background(MaterialTheme.colorScheme.primary.copy(alpha = 0.10f))) {
            val headerLabels = if (block.headers.isNotEmpty()) block.headers else List(columnCount) { "" }
            headerLabels.forEach { header ->
                Text(
                    text = header,
                    modifier = Modifier
                        .widthIn(min = 120.dp)
                        .padding(10.dp),
                    fontWeight = FontWeight.Bold,
                    style = MaterialTheme.typography.labelLarge,
                )
            }
        }
        block.rows.forEach { row ->
            HorizontalDivider()
            Row {
                val cells = row + List((columnCount - row.size).coerceAtLeast(0)) { "" }
                cells.take(columnCount).forEach { cell ->
                    Text(
                        text = cell,
                        modifier = Modifier
                            .widthIn(min = 120.dp)
                            .padding(10.dp),
                        style = MaterialTheme.typography.bodyMedium,
                    )
                }
            }
        }
    }
}

@Composable
private fun MonospaceBlock(block: LessonBlock, label: String) {
    CSNexusCard(modifier = Modifier.padding(vertical = 10.dp)) {
        Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
            CSNexusStatusBadge(text = label)
            SelectionContainer {
                Text(
                    text = block.text,
                    fontFamily = FontFamily.Monospace,
                    style = MaterialTheme.typography.bodyMedium,
                )
            }
        }
    }
}

@Composable
private fun CalloutBlock(label: String, text: String, color: Color) {
    Surface(
        modifier = Modifier
            .fillMaxWidth()
            .padding(vertical = 10.dp),
        color = color.copy(alpha = 0.10f),
        tonalElevation = 0.dp,
    ) {
        Column(Modifier.padding(14.dp)) {
            Text(label, color = color, fontWeight = FontWeight.Bold, style = MaterialTheme.typography.labelLarge)
            Text(text, modifier = Modifier.padding(top = 6.dp), style = MaterialTheme.typography.bodyMedium)
        }
    }
}

@Composable
private fun ExampleBlock(text: String) {
    var expanded by remember { mutableStateOf(true) }

    CSNexusCard(modifier = Modifier.padding(vertical = 10.dp)) {
        Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
            TextButton(
                onClick = { expanded = !expanded },
                contentPadding = PaddingValues(0.dp),
                colors = ButtonDefaults.textButtonColors(contentColor = MaterialTheme.colorScheme.onSurface),
            ) {
                Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    Icon(
                        imageVector = if (expanded) Icons.Filled.ExpandLess else Icons.Filled.ExpandMore,
                        contentDescription = null,
                    )
                    Text("Example", style = MaterialTheme.typography.titleMedium)
                }
            }
            if (expanded) {
                Text(text, style = MaterialTheme.typography.bodyMedium)
            }
        }
    }
}

@Composable
private fun StepBlock(items: List<String>) {
    CSNexusCard(modifier = Modifier.padding(vertical = 10.dp)) {
        Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
            Text("Step-by-step", color = MaterialTheme.colorScheme.primary, style = MaterialTheme.typography.labelLarge)
            items.filter { it.isNotBlank() }.forEachIndexed { index, item ->
                Text("${index + 1}. ${item.trim()}", style = MaterialTheme.typography.bodyMedium)
            }
        }
    }
}

@Composable
private fun ListBlock(items: List<String>) {
    CSNexusCard(modifier = Modifier.padding(vertical = 10.dp)) {
        Column(verticalArrangement = Arrangement.spacedBy(6.dp)) {
            items.filter { it.isNotBlank() }.forEach { item ->
                Text("- ${item.trim()}", style = MaterialTheme.typography.bodyMedium)
            }
        }
    }
}

@Composable
private fun MediaFallbackBlock(block: LessonBlock) {
    CSNexusCard(modifier = Modifier.padding(vertical = 10.dp)) {
        Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
            Text("Diagram", style = MaterialTheme.typography.titleMedium)
            Text(
                text = block.fallbackText ?: "Diagram content is available as source text below.",
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )
            if (block.text.isNotBlank()) {
                Text(block.text.take(500), fontFamily = FontFamily.Monospace, style = MaterialTheme.typography.bodySmall)
            }
        }
    }
}

@Composable
private fun CheckUnderstandingBlock(block: LessonBlock) {
    if (block.checks.isEmpty()) {
        UnknownBlock(block.copy(fallbackText = "Check activity is unavailable."))
        return
    }
    val revealed = remember { mutableStateListOf<Int>() }

    CSNexusCard(modifier = Modifier.padding(vertical = 10.dp)) {
        Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
            Text("Check your understanding", color = MaterialTheme.colorScheme.primary, fontWeight = FontWeight.Bold)
            block.checks.forEachIndexed { index, check ->
                val isOpen = index in revealed
                Column(
                    modifier = Modifier
                        .fillMaxWidth()
                        .clickable {
                            if (isOpen) revealed.remove(index) else revealed.add(index)
                        }
                        .semantics { role = Role.Button }
                        .padding(vertical = 8.dp),
                ) {
                    Text(check.question, style = MaterialTheme.typography.bodyMedium, fontWeight = FontWeight.SemiBold)
                    Row(
                        modifier = Modifier.padding(top = 4.dp),
                        horizontalArrangement = Arrangement.spacedBy(6.dp),
                    ) {
                        Text(
                            if (isOpen) "Hide answer" else "Show answer",
                            color = MaterialTheme.colorScheme.primary,
                            style = MaterialTheme.typography.labelLarge,
                        )
                        Icon(
                            imageVector = if (isOpen) Icons.Filled.ExpandLess else Icons.Filled.ExpandMore,
                            contentDescription = null,
                        )
                    }
                    if (isOpen) {
                        Text(check.answer, modifier = Modifier.padding(top = 8.dp), style = MaterialTheme.typography.bodyMedium)
                        if (check.rationale.isNotBlank()) {
                            Text(
                                check.rationale,
                                modifier = Modifier.padding(top = 4.dp),
                                color = MaterialTheme.colorScheme.onSurfaceVariant,
                                style = MaterialTheme.typography.bodySmall,
                            )
                        }
                    }
                }
            }
        }
    }
}

@Composable
private fun UnknownBlock(block: LessonBlock) {
    CalloutBlock(
        label = "Unsupported lesson block",
        text = block.fallbackText ?: block.text.ifBlank { "This content type is not available in the Android app yet." },
        color = MaterialTheme.colorScheme.error,
    )
}
