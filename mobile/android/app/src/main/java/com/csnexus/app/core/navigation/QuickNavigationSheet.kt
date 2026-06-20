package com.csnexus.app.core.navigation

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.clickable
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.Icon
import androidx.compose.material3.ListItem
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.ModalBottomSheet
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.focus.FocusRequester
import androidx.compose.ui.focus.focusRequester
import androidx.compose.ui.platform.LocalSoftwareKeyboardController
import androidx.compose.ui.semantics.Role
import androidx.compose.ui.semantics.role
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.unit.dp
import com.csnexus.app.core.design.CSNexusSearchField

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun QuickNavigationSheet(
    destinations: List<ShellDestination>,
    onNavigate: (ShellDestination) -> Unit,
    onDismiss: () -> Unit,
) {
    var query by remember { mutableStateOf("") }
    val focusRequester = remember { FocusRequester() }
    val keyboardController = LocalSoftwareKeyboardController.current
    val results = remember(query, destinations) {
        filterShellDestinations(query, destinations)
    }

    LaunchedEffect(Unit) {
        focusRequester.requestFocus()
        keyboardController?.show()
    }

    ModalBottomSheet(onDismissRequest = onDismiss) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = 20.dp, vertical = 8.dp),
            verticalArrangement = Arrangement.spacedBy(12.dp),
        ) {
            Text("Quick navigation", style = MaterialTheme.typography.titleLarge)
            CSNexusSearchField(
                value = query,
                onValueChange = { query = it },
                modifier = Modifier.focusRequester(focusRequester),
                placeholder = "Type a page or command",
            )
            if (results.isEmpty()) {
                Text(
                    text = "No matches",
                    modifier = Modifier.padding(vertical = 24.dp),
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                )
            } else {
                LazyColumn(
                    modifier = Modifier.fillMaxWidth(),
                ) {
                    ShellDestinationSection.entries.forEach { section ->
                        val sectionItems = results.filter { it.section == section }
                        if (sectionItems.isNotEmpty()) {
                            item(key = "header-${section.name}") {
                                Text(
                                    text = section.label,
                                    modifier = Modifier.padding(top = 12.dp, bottom = 4.dp),
                                    style = MaterialTheme.typography.labelLarge,
                                    color = MaterialTheme.colorScheme.primary,
                                )
                            }
                            items(sectionItems, key = { it.route.route }) { destination ->
                                ListItem(
                                    headlineContent = { Text(destination.label) },
                                    supportingContent = {
                                        Text(destination.keywords.joinToString(" / "))
                                    },
                                    leadingContent = {
                                        Icon(destination.icon, contentDescription = null)
                                    },
                                    modifier = Modifier
                                        .fillMaxWidth()
                                        .clickable { onNavigate(destination) }
                                        .semantics { role = Role.Button },
                                    trailingContent = {
                                        Row {
                                            Text(
                                                text = destination.route.route,
                                                color = MaterialTheme.colorScheme.onSurfaceVariant,
                                                style = MaterialTheme.typography.labelSmall,
                                            )
                                        }
                                    },
                                )
                                HorizontalDivider()
                            }
                        }
                    }
                }
            }
        }
    }
}
