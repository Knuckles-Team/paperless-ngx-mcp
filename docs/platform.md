# Provider boundary

This project is a client of the standard Paperless-ngx REST API. It does not deploy,
patch, seed, or customize a Paperless-ngx instance.

The connector covers the stock document, correspondent, tag, document-type,
storage-path, custom-field, saved-view, search, task, statistics, status, remote-version,
UI-settings, and schema resources used by its typed client. Instance plugins and custom
taxonomies remain external. Schema discovery can inform a reviewed future connector
change, but it never auto-persists an instance-specific ontology into this repository.
