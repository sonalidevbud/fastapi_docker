import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship

from app.db import Base

# role_permission_rel = Table(
#     "roles_permissions_link",
#     Base.metadata,
#     Column("role_id", ForeignKey("roles.id"), autoincrement=False, nullable=False, primary_key=True),
#     Column("permission_id", ForeignKey("permissions.id"), autoincrement=False, nullable=False, primary_key=True),
# )


# class Role(Base):
#     __tablename__ = "roles"
#     id = Column(INTEGER(), Identity(), primary_key=True, autoincrement=True, nullable=False)
#     role_name = Column(VARCHAR(length=100), autoincrement=False, nullable=True)
#     role_description = Column(VARCHAR(length=100), autoincrement=False, nullable=True)

#     users_FK = relationship("User", back_populates="role_FK")
#     # PrimaryKeyConstraint("id", name="roles_pkey"),
#     # UniqueConstraint("uuid", name="roles_uuid_key"),

#     permission = relationship("Permission", secondary=role_permission_rel, back_populates="role")


# class Permission(Base):
#     __tablename__ = "permissions"
#     id = Column(INTEGER(), Identity(), primary_key=True, autoincrement=True, nullable=False)
#     uuid = Column("uuid", UUID(as_uuid=True), autoincrement=False, nullable=True)
#     name = Column(VARCHAR(length=100), autoincrement=False, nullable=True)
#     title = Column(VARCHAR(length=100), autoincrement=False, nullable=True)
#     description = Column(VARCHAR(length=100), autoincrement=False, nullable=True)

#     # PrimaryKeyConstraint("id", name="permissions_pkey"),
#     # UniqueConstraint("uuid", name="permissions_uuid_key"),

#     # role = relationship("Role", secondary=role_permission_rel, back_populates="permission")


# class User(Base):
#     __tablename__ = "users"
#     id = Column(INTEGER(), Identity(), primary_key=True, autoincrement=True, nullable=False)
#     # uuid = Column(UUID(as_uuid=True), autoincrement=False, nullable=True)
#     email = Column(VARCHAR(length=256), autoincrement=False, nullable=True, unique=True)
#     first_name = Column(VARCHAR(length=100), autoincrement=False, nullable=True)
#     last_name = Column(VARCHAR(length=100), autoincrement=False, nullable=True)
#     user_role_id = Column(INTEGER(), ForeignKey("roles.id"), autoincrement=False, nullable=True)
#     created_at = Column(TIMESTAMP(timezone=True), autoincrement=False, nullable=True)
#     updated_at = Column(TIMESTAMP(timezone=True), autoincrement=False, nullable=True)

#     # role_FK = relationship("Role", back_populates="users_FK")

#     # ForeignKeyConstraint(["user_role_id"], ["roles.id"], name="role_FK"),
#     # PrimaryKeyConstraint("id", name="users_pkey"),
#     # UniqueConstraint("email", name="users_email_key"),
#     # UniqueConstraint("phone", name="users_phone_key"),


# ===============

role_permission_rel = sa.Table(
    "roles_permissions_link",
    Base.metadata,
    sa.Column("role_id", sa.ForeignKey("roles.id"), autoincrement=False, nullable=False, primary_key=True),
    sa.Column("permission_id", sa.ForeignKey("permissions.id"), autoincrement=False, nullable=False, primary_key=True),
)

users_groups_rel = sa.Table(
    "users_groups_link",
    Base.metadata,
    sa.Column("user_id", sa.ForeignKey("users.id"), autoincrement=False, nullable=False, primary_key=True),
    sa.Column("user_group_id", sa.ForeignKey("users_groups.id"), autoincrement=False, nullable=False, primary_key=True),
)


class Role(Base):
    __tablename__ = "roles"
    id = sa.Column(sa.INTEGER(), sa.Identity(), primary_key=True, autoincrement=True, nullable=False)
    uuid = sa.Column(UUID(as_uuid=True), autoincrement=False, nullable=True)
    role_name = sa.Column(sa.VARCHAR(length=100), autoincrement=False, nullable=True)
    role_title = sa.Column(sa.VARCHAR(length=100), autoincrement=False, nullable=True)
    role_description = sa.Column(sa.VARCHAR(length=100), autoincrement=False, nullable=True)
    is_custom = sa.Column(sa.BOOLEAN(), autoincrement=False, nullable=True)
    is_visible = sa.Column(sa.BOOLEAN(), autoincrement=False, nullable=True)
    users_FK = relationship("User", back_populates="role_FK")
    permission = relationship("Permission", secondary=role_permission_rel, back_populates="role")


class Permission(Base):
    __tablename__ = "permissions"
    id = sa.Column(sa.INTEGER(), sa.Identity(), primary_key=True, autoincrement=True, nullable=False)
    uuid = sa.Column(UUID(as_uuid=True), autoincrement=False, nullable=True)
    name = sa.Column(sa.VARCHAR(length=100), autoincrement=False, nullable=True)
    title = sa.Column(sa.VARCHAR(length=100), autoincrement=False, nullable=True)
    description = sa.Column(sa.VARCHAR(length=100), autoincrement=False, nullable=True)
    group = sa.Column(sa.VARCHAR(length=100), autoincrement=False, nullable=True)

    # PrimaryKeyConstraint("id", name="permissions_pkey"),
    # UniqueConstraint("uuid", name="permissions_uuid_key"),

    role = relationship("Role", secondary=role_permission_rel, back_populates="permission")


class User(Base):
    __tablename__ = "users"
    id = sa.Column(sa.INTEGER(), sa.Identity(), primary_key=True, autoincrement=True, nullable=False)
    uuid = sa.Column(UUID(as_uuid=True), autoincrement=False, nullable=True)
    email = sa.Column(sa.VARCHAR(length=256), autoincrement=False, nullable=True, unique=True)
    phone = sa.Column(sa.VARCHAR(length=16), autoincrement=False, nullable=True, unique=True)
    password = sa.Column(sa.VARCHAR(length=256), autoincrement=False, nullable=True, unique=True)
    first_name = sa.Column(sa.VARCHAR(length=100), autoincrement=False, nullable=True)
    last_name = sa.Column(sa.VARCHAR(length=100), autoincrement=False, nullable=True)
    auth_token = sa.Column(sa.VARCHAR(length=128), autoincrement=False, nullable=True, unique=True)
    auth_token_valid_to = sa.Column(sa.TIMESTAMP(timezone=True), autoincrement=False, nullable=True)
    user_role_id = sa.Column(sa.INTEGER(), sa.ForeignKey("roles.id"), autoincrement=False, nullable=True)
    is_active = sa.Column(sa.BOOLEAN(), autoincrement=False, nullable=True)
    is_verified = sa.Column(sa.BOOLEAN(), autoincrement=False, nullable=True)
    tos = sa.Column(sa.BOOLEAN(), autoincrement=False, nullable=True)
    tz = sa.Column(sa.VARCHAR(length=64), autoincrement=False, nullable=True, unique=True)
    lang = sa.Column(sa.VARCHAR(length=8), autoincrement=False, nullable=True, unique=True)
    lang = sa.Column(sa.VARCHAR(length=8), autoincrement=False, nullable=True, unique=True)
    tenant_id = sa.Column(sa.VARCHAR(length=64), autoincrement=False, nullable=True)
    created_at = sa.Column(sa.TIMESTAMP(timezone=True), autoincrement=False, nullable=True)
    updated_at = sa.Column(sa.TIMESTAMP(timezone=True), autoincrement=False, nullable=True)

    role_FK = relationship("Role", back_populates="users_FK")
    user_group = relationship("UserGroup", secondary=users_groups_rel, back_populates="users")


idea_file_rel = sa.Table(
    "ideas_files_link",
    Base.metadata,
    sa.Column("idea_id", sa.ForeignKey("ideas.id"), autoincrement=False, nullable=False, primary_key=True),
    sa.Column("file_id", sa.ForeignKey("files.id"), autoincrement=False, nullable=False, primary_key=True),
    # ForeignKeyConstraint(["file_id"], ["files.id"], name="ideas_files_link_fk_1"),
    # ForeignKeyConstraint(["idea_id"], ["ideas.id"], name="ideas_files_link_fk"),
    # PrimaryKeyConstraint("idea_id", "file_id", name="ideas_files_link_pkey"),
)


class Idea(Base):
    __tablename__ = "ideas"
    id = sa.Column(sa.INTEGER(), sa.Identity(), primary_key=True, autoincrement=True, nullable=False)
    uuid = sa.Column(UUID(as_uuid=True), autoincrement=False, nullable=True)
    author_id = sa.Column(sa.INTEGER(), autoincrement=False, nullable=True)
    upvotes = sa.Column(sa.INTEGER(), default=0, autoincrement=False, nullable=True)
    downvotes = sa.Column(sa.INTEGER(), default=0, autoincrement=False, nullable=True)
    title = sa.Column(sa.VARCHAR(length=256), autoincrement=False, nullable=True)
    description = sa.Column(sa.TEXT(), autoincrement=False, nullable=True)
    body_json = sa.Column(sa.TEXT, autoincrement=False, nullable=True)
    body_jsonb = sa.Column(JSONB, autoincrement=False, nullable=True)
    color = sa.Column(sa.VARCHAR(length=8), autoincrement=False, nullable=True)
    status = sa.Column(sa.VARCHAR(length=32), autoincrement=False, nullable=True)
    created_at = sa.Column(sa.TIMESTAMP(timezone=True), autoincrement=False, nullable=True)
    updated_at = sa.Column(sa.TIMESTAMP(timezone=True), autoincrement=False, nullable=True)
    deleted_at = sa.Column(sa.TIMESTAMP(timezone=True), autoincrement=False, nullable=True)

    pictures = relationship("File", secondary=idea_file_rel, back_populates="idea")


class File(Base):
    __tablename__ = "files"
    id = sa.Column(sa.INTEGER(), sa.Identity(), primary_key=True, autoincrement=True, nullable=False)
    uuid = sa.Column(UUID(as_uuid=True), autoincrement=False, nullable=True)
    owner_id = sa.Column(sa.INTEGER(), autoincrement=False, nullable=True)
    file_name = sa.Column(sa.VARCHAR(length=256), autoincrement=False, nullable=True)
    file_description = sa.Column(sa.VARCHAR(length=256), autoincrement=False, nullable=True)
    extension = sa.Column(sa.VARCHAR(length=8), autoincrement=False, nullable=True)
    mimetype = sa.Column(sa.VARCHAR(length=256), autoincrement=False, nullable=True)
    size = sa.Column(sa.INTEGER(), autoincrement=False, nullable=True)
    created_at = sa.Column(sa.TIMESTAMP(timezone=True), autoincrement=False, nullable=True)
    updated_at = sa.Column(sa.TIMESTAMP(timezone=True), autoincrement=False, nullable=True)
    deleted_at = sa.Column(sa.TIMESTAMP(timezone=True), autoincrement=False, nullable=True)

    idea = relationship("Idea", secondary=idea_file_rel, back_populates="pictures")


class Setting(Base):
    __tablename__ = "settings"
    id = sa.Column(sa.INTEGER(), sa.Identity(), primary_key=True, autoincrement=True, nullable=False)
    name = sa.Column(sa.VARCHAR(length=256), unique=True, autoincrement=False, nullable=True)
    value = sa.Column(sa.VARCHAR(length=256), autoincrement=False, nullable=True)
    value_type = sa.Column(sa.VARCHAR(length=64), autoincrement=False, nullable=True)
    prev_value = sa.Column(sa.VARCHAR(length=256), autoincrement=False, nullable=True)
    descripton = sa.Column(sa.VARCHAR(length=256), autoincrement=False, nullable=True)
    updated_by = sa.Column(sa.VARCHAR(length=256), autoincrement=False, nullable=True)
    created_at = sa.Column(sa.TIMESTAMP(timezone=True), autoincrement=False, nullable=True)
    updated_at = sa.Column(sa.TIMESTAMP(timezone=True), autoincrement=False, nullable=True)


class UserGroup(Base):
    __tablename__ = "users_groups"
    id = sa.Column(sa.INTEGER(), sa.Identity(), primary_key=True, autoincrement=True, nullable=False)
    uuid = sa.Column(UUID(as_uuid=True), autoincrement=False, nullable=True)
    name = sa.Column(sa.VARCHAR(length=256), autoincrement=False, nullable=True)
    description = sa.Column(sa.VARCHAR(length=512), autoincrement=False, nullable=True)
    created_at = sa.Column(sa.TIMESTAMP(timezone=True), autoincrement=False, nullable=True)
    updated_at = sa.Column(sa.TIMESTAMP(timezone=True), autoincrement=False, nullable=True)
    # users_FK = relationship("User", back_populates="role_FK")
    # permission = relationship("Permission", secondary=role_permission_rel, back_populates="role")

    users = relationship("User", secondary=users_groups_rel, back_populates="user_group")  # Roles
