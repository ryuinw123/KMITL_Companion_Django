# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Admin(models.Model):
    username = models.CharField(primary_key=True, max_length=255)
    password = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'admin'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Bookmark(models.Model):
    bookmark_student = models.OneToOneField('User', models.DO_NOTHING, primary_key=True)
    bookmark_marker = models.ForeignKey('Marker', models.DO_NOTHING)
    createtime = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bookmark'
        unique_together = (('bookmark_student', 'bookmark_marker'),)


class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    content = models.TextField(blank=True, null=True)
    comment_marker = models.ForeignKey('Marker', models.DO_NOTHING, blank=True, null=True)
    comment_student = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)
    createtime = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'comment'


class CommentLike(models.Model):
    cl_comment = models.ForeignKey(Comment, models.DO_NOTHING)
    cl_student = models.ForeignKey('User', models.DO_NOTHING)
    createtime = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'comment_like'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Emergency(models.Model):
    contact_id = models.AutoField(primary_key=True)
    contact_number = models.CharField(max_length=45, blank=True, null=True)
    contact_name = models.CharField(max_length=45, blank=True, null=True)
    contact_admin_username = models.ForeignKey(Admin, models.DO_NOTHING, db_column='contact_admin_username', blank=True, null=True)
    createdtime = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'emergency'


class Event(models.Model):
    event_id = models.AutoField(primary_key=True)
    eventname = models.CharField(max_length=255)
    starttime = models.DateTimeField(blank=True, null=True)
    endtime = models.DateTimeField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    student = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)
    marker = models.ForeignKey('Marker', models.DO_NOTHING, blank=True, null=True)
    createtime = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'event'


class Issue(models.Model):
    issue_id = models.AutoField(primary_key=True)
    description = models.TextField(blank=True, null=True)
    imageurl = models.TextField(blank=True, null=True)
    createtime = models.DateTimeField(blank=True, null=True)
    issue_user = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)
    issue_marker = models.ForeignKey('Marker', models.DO_NOTHING, blank=True, null=True)
    issue_approve_admin_username = models.ForeignKey(Admin, models.DO_NOTHING, db_column='issue_approve_admin_username',related_name='issue_approve_admin_username', blank=True, null=True)
    issue_broadcast_admin_username = models.ForeignKey(Admin, models.DO_NOTHING, db_column ='issue_broadcast_admin_username',related_name='issue_broadcast_admin_username', blank=True, null=True)
    broadcasttime = models.DateTimeField(blank=True, null=True)
    approvetime = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'issue'


class Marker(models.Model):
    marker_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    lat = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    long = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    tag = models.CharField(max_length=45, blank=True, null=True)
    imageurl = models.TextField(db_column='imageURL', blank=True, null=True)  # Field name made lowercase.
    enable = models.IntegerField(blank=True, null=True)
    created_admin = models.ForeignKey(Admin, models.DO_NOTHING, blank=True, null=True)
    created_user = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)
    approve_admin_username = models.ForeignKey(Admin, models.DO_NOTHING, db_column='approve_admin_username',related_name ='approve_admin_username', blank=True, null=True)
    createtime = models.DateTimeField(blank=True, null=True)
    approvetime = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'marker'


class MarkerLike(models.Model):
    markerlike_student = models.OneToOneField('User', models.DO_NOTHING, primary_key=True)
    markerlike_marker = models.ForeignKey(Marker, models.DO_NOTHING)
    createtime = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'marker_like'
        unique_together = (('markerlike_student', 'markerlike_marker'),)


class News(models.Model):
    news_id = models.AutoField(primary_key=True)
    header = models.TextField(blank=True, null=True)
    body = models.TextField(blank=True, null=True)
    imageurl = models.TextField(blank=True, null=True)
    createdtime = models.DateTimeField(blank=True, null=True)
    n_created_admin_username = models.ForeignKey(Admin, models.DO_NOTHING, db_column='n_created_admin_username',related_name='n_created_admin_username', blank=True, null=True)
    n_broadcast_admin_username = models.ForeignKey(Admin, models.DO_NOTHING, db_column="n_broadcast_admin_username",related_name ='n_broadcast_admin_username', blank=True, null=True)
    broadcasttime = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'news'


class Permission(models.Model):
    permission_id = models.AutoField(primary_key=True)
    permission_student = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)
    createtime = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'permission'


class PermissionMarker(models.Model):
    pm_permission = models.OneToOneField(Permission, models.DO_NOTHING, primary_key=True)
    pm_maker = models.ForeignKey(Marker, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'permission_marker'


class User(models.Model):
    student_id = models.IntegerField(primary_key=True)
    firstname = models.CharField(max_length=255, blank=True, null=True)
    lastname = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255)
    token = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user'
