"""Surface contracts: tool use, links, data locations and business roles."""

from scion_sdk.surface_contracts import (
    BusinessRole,
    DataLocation,
    Refusal,
    SurfaceLink,
    ToolStep,
    ToolUseContract,
)

CONTRACTS = (
    ToolUseContract(
        "find-and-read-a-document",
        (
            ToolStep(
                "paperless_ngx_global_search",
                params=("query", "db_only"),
                result=("documents", "correspondents", "tags"),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED",
                        "the token is rejected or the operation is forbidden",
                    ),
                ),
            ),
            ToolStep(
                "paperless_ngx_autocomplete",
                params=("term", "limit"),
                result=("terms",),
            ),
            ToolStep(
                "paperless_ngx_list_documents",
                params=("query", "ordering", "page_size", "max_pages", "filters"),
                result=("id", "title", "correspondent", "tags", "created"),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED",
                        "the token is rejected or the operation is forbidden",
                    ),
                ),
            ),
            ToolStep(
                "paperless_ngx_get_document",
                params=("document_id",),
                result=(
                    "id",
                    "title",
                    "content",
                    "tags",
                    "correspondent",
                    "document_type",
                ),
                refusals=(Refusal("NOT_FOUND", "no object has the id"),),
            ),
            ToolStep(
                "paperless_ngx_get_document_metadata",
                params=("document_id",),
                result=("original_checksum", "media_filename", "archive_metadata"),
                refusals=(Refusal("NOT_FOUND", "no object has the id"),),
            ),
            ToolStep(
                "paperless_ngx_get_document_notes",
                params=("document_id",),
                result=("id", "note", "created"),
                refusals=(Refusal("NOT_FOUND", "no object has the id"),),
            ),
        ),
    ),
    ToolUseContract(
        "intake-a-document",
        (
            ToolStep(
                "paperless_ngx_post_document",
                params=(
                    "file_path",
                    "title",
                    "correspondent",
                    "document_type",
                    "tags",
                    "created",
                ),
                result=("task_id",),
                refusals=(
                    Refusal(
                        "OUTSIDE_WORKSPACE",
                        "the file is missing, oversized or outside the configured workspace",
                    ),
                    Refusal(
                        "ACCESS_DENIED",
                        "the token is rejected or the operation is forbidden",
                    ),
                ),
            ),
            ToolStep(
                "paperless_ngx_get_task",
                params=("task_id",),
                result=("status", "related_document", "result"),
                refusals=(Refusal("NOT_FOUND", "no task has the id"),),
            ),
            ToolStep(
                "paperless_ngx_list_tasks",
                params=("status", "max_pages"),
                result=("task_id", "status", "task_file_name"),
            ),
            ToolStep(
                "paperless_ngx_acknowledge_tasks",
                params=("tasks",),
                result=("acknowledged",),
            ),
            ToolStep(
                "paperless_ngx_get_document",
                params=("document_id",),
                result=("id", "title", "created"),
                refusals=(Refusal("NOT_FOUND", "no object has the id"),),
            ),
        ),
    ),
    ToolUseContract(
        "edit-document-metadata",
        (
            ToolStep(
                "paperless_ngx_list_correspondents",
                params=("name__icontains", "max_pages"),
                result=("id", "name"),
            ),
            ToolStep(
                "paperless_ngx_list_tags",
                params=("name__icontains", "max_pages"),
                result=("id", "name"),
            ),
            ToolStep(
                "paperless_ngx_list_document_types",
                params=("name__icontains", "max_pages"),
                result=("id", "name"),
            ),
            ToolStep(
                "paperless_ngx_list_storage_paths",
                params=("name__icontains", "max_pages"),
                result=("id", "name", "path"),
            ),
            ToolStep(
                "paperless_ngx_get_document",
                params=("document_id",),
                result=("id", "title", "tags", "correspondent"),
                refusals=(Refusal("NOT_FOUND", "no object has the id"),),
            ),
            ToolStep(
                "paperless_ngx_update_document",
                params=("document_id", "body"),
                result=("id", "title", "tags", "correspondent", "document_type"),
                refusals=(
                    Refusal("NOT_FOUND", "no object has the id"),
                    Refusal(
                        "INVALID_BODY",
                        "the body names a field or id the instance rejects",
                    ),
                ),
            ),
            ToolStep(
                "paperless_ngx_add_document_note",
                params=("document_id", "note"),
                result=("notes",),
                refusals=(Refusal("NOT_FOUND", "no object has the id"),),
            ),
        ),
    ),
    ToolUseContract(
        "bulk-edit-documents",
        (
            ToolStep(
                "paperless_ngx_list_documents",
                params=("query", "page_size", "max_pages", "filters"),
                result=("id", "title", "tags"),
            ),
            ToolStep(
                "paperless_ngx_bulk_edit_documents",
                params=("documents", "method", "parameters"),
                result=("affected_documents",),
                refusals=(
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the user has not approved the document set and method",
                    ),
                    Refusal(
                        "INVALID_METHOD", "the method or parameters are not accepted"
                    ),
                ),
            ),
        ),
    ),
    ToolUseContract(
        "remove-a-document",
        (
            ToolStep(
                "paperless_ngx_get_document",
                params=("document_id",),
                result=("id", "title"),
                refusals=(Refusal("NOT_FOUND", "no object has the id"),),
            ),
            ToolStep(
                "paperless_ngx_delete_document",
                params=("document_id",),
                result=("status",),
                refusals=(
                    Refusal("NOT_FOUND", "no object has the id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the user has not approved moving the document to the trash",
                    ),
                ),
            ),
        ),
    ),
    ToolUseContract(
        "create-a-document-record",
        (
            ToolStep(
                "paperless_ngx_create_document",
                params=("body",),
                result=("id", "title"),
                refusals=(
                    Refusal(
                        "INVALID_BODY",
                        "the body is missing a required field or names an unknown id",
                    ),
                ),
            ),
            ToolStep(
                "paperless_ngx_get_document",
                params=("document_id",),
                result=("id", "title", "created"),
                refusals=(Refusal("NOT_FOUND", "no object has the id"),),
            ),
        ),
    ),
    ToolUseContract(
        "curate-correspondents",
        (
            ToolStep(
                "paperless_ngx_list_correspondents",
                params=("name__icontains", "max_pages"),
                result=("id", "name", "document_count"),
            ),
            ToolStep(
                "paperless_ngx_create_correspondent",
                params=("body",),
                result=("id", "name"),
                refusals=(
                    Refusal("DUPLICATE", "a correspondent with the name exists"),
                ),
            ),
            ToolStep(
                "paperless_ngx_update_correspondent",
                params=("correspondent_id", "body"),
                result=("id", "name"),
                refusals=(Refusal("NOT_FOUND", "no object has the id"),),
            ),
            ToolStep(
                "paperless_ngx_delete_correspondent",
                params=("correspondent_id",),
                result=("status",),
                refusals=(
                    Refusal("NOT_FOUND", "no object has the id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the user has not approved the deletion",
                    ),
                ),
            ),
        ),
    ),
    ToolUseContract(
        "curate-tags",
        (
            ToolStep(
                "paperless_ngx_list_tags",
                params=("name__icontains", "max_pages"),
                result=("id", "name", "color", "document_count"),
            ),
            ToolStep(
                "paperless_ngx_create_tag",
                params=("body",),
                result=("id", "name"),
                refusals=(Refusal("DUPLICATE", "a tag with the name exists"),),
            ),
            ToolStep(
                "paperless_ngx_update_tag",
                params=("tag_id", "body"),
                result=("id", "name", "color"),
                refusals=(Refusal("NOT_FOUND", "no object has the id"),),
            ),
            ToolStep(
                "paperless_ngx_delete_tag",
                params=("tag_id",),
                result=("status",),
                refusals=(
                    Refusal("NOT_FOUND", "no object has the id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the user has not approved the deletion",
                    ),
                ),
            ),
        ),
    ),
    ToolUseContract(
        "curate-document-types",
        (
            ToolStep(
                "paperless_ngx_list_document_types",
                params=("name__icontains", "max_pages"),
                result=("id", "name", "document_count"),
            ),
            ToolStep(
                "paperless_ngx_create_document_type",
                params=("body",),
                result=("id", "name"),
                refusals=(
                    Refusal("DUPLICATE", "a document type with the name exists"),
                ),
            ),
            ToolStep(
                "paperless_ngx_delete_document_type",
                params=("document_type_id",),
                result=("status",),
                refusals=(
                    Refusal("NOT_FOUND", "no object has the id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the user has not approved the deletion",
                    ),
                ),
            ),
        ),
    ),
    ToolUseContract(
        "curate-storage-paths-and-fields",
        (
            ToolStep(
                "paperless_ngx_list_storage_paths",
                params=("name__icontains", "max_pages"),
                result=("id", "name", "path"),
            ),
            ToolStep(
                "paperless_ngx_create_storage_path",
                params=("body",),
                result=("id", "name", "path"),
                refusals=(Refusal("DUPLICATE", "a storage path with the name exists"),),
            ),
            ToolStep(
                "paperless_ngx_list_custom_fields",
                params=("max_pages",),
                result=("id", "name", "data_type"),
            ),
            ToolStep(
                "paperless_ngx_create_custom_field",
                params=("body",),
                result=("id", "name", "data_type"),
                refusals=(Refusal("DUPLICATE", "a custom field with the name exists"),),
            ),
            ToolStep(
                "paperless_ngx_list_saved_views",
                params=("max_pages",),
                result=("id", "name", "filter_rules"),
            ),
        ),
    ),
    ToolUseContract(
        "inspect-system-health",
        (
            ToolStep(
                "paperless_ngx_get_system_status",
                result=("pngx_version", "database", "tasks", "storage"),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED",
                        "the token is rejected or the operation is forbidden",
                    ),
                ),
            ),
            ToolStep(
                "paperless_ngx_get_statistics",
                result=("documents_total", "documents_inbox", "character_count"),
            ),
            ToolStep(
                "paperless_ngx_get_remote_version",
                result=("version", "update_available"),
            ),
            ToolStep(
                "paperless_ngx_get_ui_settings",
                result=("user", "permissions", "settings"),
            ),
            ToolStep(
                "paperless_ngx_get_schema",
                result=("openapi", "paths"),
            ),
            ToolStep(
                "paperless_ngx_list_tasks",
                params=("status", "max_pages"),
                result=("task_id", "status", "task_file_name"),
            ),
        ),
    ),
    ToolUseContract(
        "sync-structure-to-graph",
        (
            ToolStep(
                "paperless_ingestion_projection",
                params=("params_json",),
                result=("records", "relationships"),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED",
                        "the token is rejected or the operation is forbidden",
                    ),
                ),
            ),
            ToolStep(
                "paperless_ingest_projection",
                params=("params_json",),
                result=("ingested",),
                refusals=(
                    Refusal(
                        "NO_ENGINE",
                        "no knowledge-graph engine is reachable, ingested is null",
                    ),
                ),
            ),
        ),
    ),
)

LINKS = (
    SurfaceLink(
        "find-and-read-a-document",
        tools=(
            "paperless_ngx_global_search",
            "paperless_ngx_autocomplete",
            "paperless_ngx_list_documents",
            "paperless_ngx_get_document",
            "paperless_ngx_get_document_metadata",
            "paperless_ngx_get_document_notes",
        ),
        prompts=("paperless-ngx-operator", "paperless-ngx-archivist"),
        skills=("paperless-ngx-document-management",),
    ),
    SurfaceLink(
        "intake-a-document",
        tools=(
            "paperless_ngx_post_document",
            "paperless_ngx_get_task",
            "paperless_ngx_list_tasks",
            "paperless_ngx_acknowledge_tasks",
            "paperless_ngx_get_document",
        ),
        prompts=("paperless-ngx-operator", "paperless-ngx-archivist"),
        skills=("paperless-ngx-document-management",),
    ),
    SurfaceLink(
        "edit-document-metadata",
        tools=(
            "paperless_ngx_list_correspondents",
            "paperless_ngx_list_tags",
            "paperless_ngx_list_document_types",
            "paperless_ngx_list_storage_paths",
            "paperless_ngx_get_document",
            "paperless_ngx_update_document",
            "paperless_ngx_add_document_note",
        ),
        prompts=("paperless-ngx-operator", "paperless-ngx-archivist"),
        skills=("paperless-ngx-document-management", "paperless-ngx-metadata-curation"),
    ),
    SurfaceLink(
        "bulk-edit-documents",
        tools=("paperless_ngx_list_documents", "paperless_ngx_bulk_edit_documents"),
        prompts=("paperless-ngx-operator", "paperless-ngx-archivist"),
        skills=("paperless-ngx-document-management",),
    ),
    SurfaceLink(
        "remove-a-document",
        tools=("paperless_ngx_get_document", "paperless_ngx_delete_document"),
        prompts=("paperless-ngx-operator", "paperless-ngx-archivist"),
        skills=("paperless-ngx-document-management",),
    ),
    SurfaceLink(
        "create-a-document-record",
        tools=("paperless_ngx_create_document", "paperless_ngx_get_document"),
        prompts=("paperless-ngx-operator", "paperless-ngx-archivist"),
        skills=("paperless-ngx-document-management",),
    ),
    SurfaceLink(
        "curate-correspondents",
        tools=(
            "paperless_ngx_list_correspondents",
            "paperless_ngx_create_correspondent",
            "paperless_ngx_update_correspondent",
            "paperless_ngx_delete_correspondent",
        ),
        prompts=("paperless-ngx-operator", "paperless-ngx-taxonomy-curator"),
        skills=("paperless-ngx-metadata-curation",),
    ),
    SurfaceLink(
        "curate-tags",
        tools=(
            "paperless_ngx_list_tags",
            "paperless_ngx_create_tag",
            "paperless_ngx_update_tag",
            "paperless_ngx_delete_tag",
        ),
        prompts=("paperless-ngx-operator", "paperless-ngx-taxonomy-curator"),
        skills=("paperless-ngx-metadata-curation",),
    ),
    SurfaceLink(
        "curate-document-types",
        tools=(
            "paperless_ngx_list_document_types",
            "paperless_ngx_create_document_type",
            "paperless_ngx_delete_document_type",
        ),
        prompts=("paperless-ngx-operator", "paperless-ngx-taxonomy-curator"),
        skills=("paperless-ngx-metadata-curation",),
    ),
    SurfaceLink(
        "curate-storage-paths-and-fields",
        tools=(
            "paperless_ngx_list_storage_paths",
            "paperless_ngx_create_storage_path",
            "paperless_ngx_list_custom_fields",
            "paperless_ngx_create_custom_field",
            "paperless_ngx_list_saved_views",
        ),
        prompts=("paperless-ngx-operator", "paperless-ngx-taxonomy-curator"),
        skills=("paperless-ngx-metadata-curation",),
    ),
    SurfaceLink(
        "inspect-system-health",
        tools=(
            "paperless_ngx_get_system_status",
            "paperless_ngx_get_statistics",
            "paperless_ngx_get_remote_version",
            "paperless_ngx_get_ui_settings",
            "paperless_ngx_get_schema",
            "paperless_ngx_list_tasks",
        ),
        prompts=("paperless-ngx-operator", "paperless-ngx-system-administrator"),
        skills=("paperless-ngx-system-status",),
    ),
    SurfaceLink(
        "sync-structure-to-graph",
        tools=("paperless_ingestion_projection", "paperless_ingest_projection"),
        prompts=("paperless-ngx-operator", "paperless-ngx-system-administrator"),
        skills=("paperless-ngx-kg-ingestion",),
    ),
    SurfaceLink(
        "paperless-ngx-operations",
        tools=(
            "paperless_ngx_list_documents",
            "paperless_ngx_get_document",
            "paperless_ngx_update_document",
            "paperless_ngx_post_document",
            "paperless_ngx_get_task",
            "paperless_ngx_bulk_edit_documents",
        ),
        skills=("paperless-ngx-operations",),
    ),
)

LOCATIONS = (
    DataLocation(
        "paperless-documents",
        ("PaperlessDocumentReference",),
        "PAPERLESS_URL",
        "paperless_ngx_list_documents",
        federation_key="id",
    ),
    DataLocation(
        "paperless-taxonomy",
        (
            "PaperlessCorrespondentReference",
            "PaperlessTagReference",
            "PaperlessDocumentTypeReference",
            "PaperlessStoragePathReference",
        ),
        "PAPERLESS_URL",
        "paperless_ngx_list_tags",
        federation_key="id",
    ),
    DataLocation(
        "paperless-tasks",
        ("PaperlessConsumptionTask",),
        "PAPERLESS_URL",
        "paperless_ngx_list_tasks",
        federation_key="task_id",
    ),
)

ROLES = (
    BusinessRole(
        "archivist",
        tasks=(
            "find-and-read-a-document",
            "intake-a-document",
            "edit-document-metadata",
            "bulk-edit-documents",
            "remove-a-document",
            "create-a-document-record",
        ),
    ),
    BusinessRole(
        "taxonomy-curator",
        tasks=(
            "curate-correspondents",
            "curate-tags",
            "curate-document-types",
            "curate-storage-paths-and-fields",
        ),
    ),
    BusinessRole(
        "system-administrator",
        tasks=("inspect-system-health", "sync-structure-to-graph"),
    ),
)
