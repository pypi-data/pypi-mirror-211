"""v0.34a2."""
import sqlalchemy as sa  # noqa
import sqlmodel  # noqa
from alembic import op

from lnschema_core.dev.sqlmodel import get_sqlite_prefix_schema_delim_from_alembic

revision = "1c49c9f9a982"
down_revision = "c3f38ffe9e03"


def upgrade() -> None:
    sqlite, prefix, schema, delim = get_sqlite_prefix_schema_delim_from_alembic()

    op.drop_index(f"ix_core{delim}features_created_at", table_name="lnschema_core_features")
    op.drop_index(f"ix_core{delim}features_created_by_id", table_name="lnschema_core_features")
    op.create_index(op.f("ix_lnschema_core_features_created_at"), "lnschema_core_features", ["created_at"], unique=False)
    op.create_index(op.f("ix_lnschema_core_features_created_by_id"), "lnschema_core_features", ["created_by_id"], unique=False)
    op.drop_index(f"ix_core{delim}file_created_at", table_name="lnschema_core_file")
    op.drop_index(f"ix_core{delim}file_created_by_id", table_name="lnschema_core_file")
    op.drop_index(f"ix_core{delim}file_hash", table_name="lnschema_core_file")
    op.drop_index(f"ix_core{delim}file_key", table_name="lnschema_core_file")
    op.drop_index(f"ix_core{delim}file_name", table_name="lnschema_core_file")
    op.drop_index(f"ix_core{delim}file_run_id", table_name="lnschema_core_file")
    op.drop_index(f"ix_core{delim}file_size", table_name="lnschema_core_file")
    op.drop_index(f"ix_core{delim}file_storage_id", table_name="lnschema_core_file")
    op.drop_index(f"ix_core{delim}file_suffix", table_name="lnschema_core_file")
    op.drop_index(f"ix_core{delim}file_transform_id", table_name="lnschema_core_file")
    op.drop_index(f"ix_core{delim}file_transform_version", table_name="lnschema_core_file")
    op.drop_index(f"ix_core{delim}file_updated_at", table_name="lnschema_core_file")
    op.create_index(op.f("ix_lnschema_core_file_created_at"), "lnschema_core_file", ["created_at"], unique=False)
    op.create_index(op.f("ix_lnschema_core_file_created_by_id"), "lnschema_core_file", ["created_by_id"], unique=False)
    op.create_index(op.f("ix_lnschema_core_file_hash"), "lnschema_core_file", ["hash"], unique=False)
    op.create_index(op.f("ix_lnschema_core_file_key"), "lnschema_core_file", ["key"], unique=False)
    op.create_index(op.f("ix_lnschema_core_file_name"), "lnschema_core_file", ["name"], unique=False)
    op.create_index(op.f("ix_lnschema_core_file_run_id"), "lnschema_core_file", ["run_id"], unique=False)
    op.create_index(op.f("ix_lnschema_core_file_size"), "lnschema_core_file", ["size"], unique=False)
    op.create_index(op.f("ix_lnschema_core_file_storage_id"), "lnschema_core_file", ["storage_id"], unique=False)
    op.create_index(op.f("ix_lnschema_core_file_suffix"), "lnschema_core_file", ["suffix"], unique=False)
    op.create_index(op.f("ix_lnschema_core_file_transform_id"), "lnschema_core_file", ["transform_id"], unique=False)
    op.create_index(op.f("ix_lnschema_core_file_transform_version"), "lnschema_core_file", ["transform_version"], unique=False)
    op.create_index(op.f("ix_lnschema_core_file_updated_at"), "lnschema_core_file", ["updated_at"], unique=False)
    op.drop_index(f"ix_core{delim}folder_created_at", table_name="lnschema_core_folder")
    op.drop_index(f"ix_core{delim}folder_created_by_id", table_name="lnschema_core_folder")
    op.drop_index(f"ix_core{delim}folder_key", table_name="lnschema_core_folder")
    op.drop_index(f"ix_core{delim}folder_name", table_name="lnschema_core_folder")
    op.drop_index(f"ix_core{delim}folder_storage_id", table_name="lnschema_core_folder")
    op.drop_index(f"ix_core{delim}folder_updated_at", table_name="lnschema_core_folder")
    op.create_index(op.f("ix_lnschema_core_folder_created_at"), "lnschema_core_folder", ["created_at"], unique=False)
    op.create_index(op.f("ix_lnschema_core_folder_created_by_id"), "lnschema_core_folder", ["created_by_id"], unique=False)
    op.create_index(op.f("ix_lnschema_core_folder_key"), "lnschema_core_folder", ["key"], unique=False)
    op.create_index(op.f("ix_lnschema_core_folder_name"), "lnschema_core_folder", ["name"], unique=False)
    op.create_index(op.f("ix_lnschema_core_folder_storage_id"), "lnschema_core_folder", ["storage_id"], unique=False)
    op.create_index(op.f("ix_lnschema_core_folder_updated_at"), "lnschema_core_folder", ["updated_at"], unique=False)
    op.drop_index(f"ix_core{delim}project_created_at", table_name="lnschema_core_project")
    op.drop_index(f"ix_core{delim}project_created_by_id", table_name="lnschema_core_project")
    op.drop_index(f"ix_core{delim}project_name", table_name="lnschema_core_project")
    op.drop_index(f"ix_core{delim}project_updated_at", table_name="lnschema_core_project")
    op.create_index(op.f("ix_lnschema_core_project_created_at"), "lnschema_core_project", ["created_at"], unique=False)
    op.create_index(op.f("ix_lnschema_core_project_created_by_id"), "lnschema_core_project", ["created_by_id"], unique=False)
    op.create_index(op.f("ix_lnschema_core_project_name"), "lnschema_core_project", ["name"], unique=False)
    op.create_index(op.f("ix_lnschema_core_project_updated_at"), "lnschema_core_project", ["updated_at"], unique=False)
    op.drop_index(f"ix_core{delim}run_created_at", table_name="lnschema_core_run")
    op.drop_index(f"ix_core{delim}run_created_by_id", table_name="lnschema_core_run")
    op.drop_index(f"ix_core{delim}run_external_id", table_name="lnschema_core_run")
    op.drop_index(f"ix_core{delim}run_name", table_name="lnschema_core_run")
    try:
        op.drop_index(f"ix_core{delim}run_transform_id", table_name="lnschema_core_run")
    except Exception:
        pass
    op.drop_index(f"ix_core{delim}run_transform_version", table_name="lnschema_core_run")
    op.create_index(op.f("ix_lnschema_core_run_created_at"), "lnschema_core_run", ["created_at"], unique=False)
    op.create_index(op.f("ix_lnschema_core_run_created_by_id"), "lnschema_core_run", ["created_by_id"], unique=False)
    op.create_index(op.f("ix_lnschema_core_run_external_id"), "lnschema_core_run", ["external_id"], unique=False)
    op.create_index(op.f("ix_lnschema_core_run_name"), "lnschema_core_run", ["name"], unique=False)
    op.create_index(op.f("ix_lnschema_core_run_transform_id"), "lnschema_core_run", ["transform_id"], unique=False)
    op.create_index(op.f("ix_lnschema_core_run_transform_version"), "lnschema_core_run", ["transform_version"], unique=False)
    try:
        op.drop_index(f"ix_core{delim}storage_created_at", table_name="lnschema_core_storage")
        op.drop_index(f"ix_core{delim}storage_created_by_id", table_name="lnschema_core_storage")
        op.drop_index(f"ix_core{delim}storage_root", table_name="lnschema_core_storage")
        op.drop_index(f"ix_core{delim}storage_updated_at", table_name="lnschema_core_storage")
    except Exception:
        pass
    op.create_index(op.f("ix_lnschema_core_storage_created_at"), "lnschema_core_storage", ["created_at"], unique=False)
    op.create_index(op.f("ix_lnschema_core_storage_created_by_id"), "lnschema_core_storage", ["created_by_id"], unique=False)
    op.create_index(op.f("ix_lnschema_core_storage_root"), "lnschema_core_storage", ["root"], unique=False)
    op.create_index(op.f("ix_lnschema_core_storage_updated_at"), "lnschema_core_storage", ["updated_at"], unique=False)
    op.drop_index(f"ix_core{delim}transform_created_at", table_name="lnschema_core_transform")
    op.drop_index(f"ix_core{delim}transform_created_by_id", table_name="lnschema_core_transform")
    op.drop_index(f"ix_core{delim}transform_name", table_name="lnschema_core_transform")
    try:
        op.drop_index(f"ix_core{delim}transform_reference", table_name="lnschema_core_transform")
        op.drop_index(f"ix_core{delim}transform_title", table_name="lnschema_core_transform")
        op.drop_index(f"ix_core{delim}transform_type", table_name="lnschema_core_transform")
        op.drop_index(f"ix_core{delim}transform_updated_at", table_name="lnschema_core_transform")
    except Exception:
        pass
    op.create_index(op.f("ix_lnschema_core_transform_created_at"), "lnschema_core_transform", ["created_at"], unique=False)
    op.create_index(op.f("ix_lnschema_core_transform_created_by_id"), "lnschema_core_transform", ["created_by_id"], unique=False)
    op.create_index(op.f("ix_lnschema_core_transform_name"), "lnschema_core_transform", ["name"], unique=False)
    op.create_index(op.f("ix_lnschema_core_transform_reference"), "lnschema_core_transform", ["reference"], unique=False)
    op.create_index(op.f("ix_lnschema_core_transform_title"), "lnschema_core_transform", ["title"], unique=False)
    op.create_index(op.f("ix_lnschema_core_transform_type"), "lnschema_core_transform", ["type"], unique=False)
    op.create_index(op.f("ix_lnschema_core_transform_updated_at"), "lnschema_core_transform", ["updated_at"], unique=False)
    op.drop_index(f"ix_core{delim}user_created_at", table_name="lnschema_core_user")
    op.drop_index(f"ix_core{delim}user_email", table_name="lnschema_core_user")
    op.drop_index(f"ix_core{delim}user_handle", table_name="lnschema_core_user")
    op.drop_index(f"ix_core{delim}user_name", table_name="lnschema_core_user")
    op.drop_index(f"ix_core{delim}user_updated_at", table_name="lnschema_core_user")
    op.create_index(op.f("ix_lnschema_core_user_created_at"), "lnschema_core_user", ["created_at"], unique=False)
    op.create_index(op.f("ix_lnschema_core_user_email"), "lnschema_core_user", ["email"], unique=True)
    op.create_index(op.f("ix_lnschema_core_user_handle"), "lnschema_core_user", ["handle"], unique=True)
    op.create_index(op.f("ix_lnschema_core_user_name"), "lnschema_core_user", ["name"], unique=False)
    op.create_index(op.f("ix_lnschema_core_user_updated_at"), "lnschema_core_user", ["updated_at"], unique=False)


def downgrade() -> None:
    pass
