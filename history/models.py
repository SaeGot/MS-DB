from django.db import models


class Member(models.Model):
    member_name = models.CharField(max_length=10)
    member_class = models.IntegerField(null=True)

    class Meta:
        db_table = 'history_member'

    def __str__(self):
        return self.member_name


class MemberSummary(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    member_summary_created = models.DateTimeField(auto_now_add=True)
    member_summary = models.TextField(null=True)

    class Meta:
        db_table = 'history_member_summary'

    def __str__(self):
        return self.member_summary


class PlayType(models.Model):
    play_type_name = models.CharField(max_length=30)
    play_type_description = models.CharField(max_length=30, null=True, blank=True)

    class Meta:
        db_table = 'history_play_type'

    def __str__(self):
        return self.play_type_name


class PlayTypeAlias(models.Model):
    play_type = models.ForeignKey(PlayType, on_delete=models.CASCADE)
    keyword = models.CharField(max_length=100)

    class Meta:
        db_table = 'history_play_type_alias'

    def __str__(self):
        return self.keyword


class Play(models.Model):
    play_name = models.CharField(max_length=50)
    play_date = models.DateField(null=True)
    play_type = models.ForeignKey(PlayType, on_delete=models.SET_NULL, null=True)
    play_summary = models.TextField(null=True)

    class Meta:
        db_table = 'history_play'

    def __str__(self):
        return self.play_name


class PlaySummary(models.Model):
    play = models.ForeignKey(Play, on_delete=models.CASCADE)
    play_summary_created = models.DateTimeField(auto_now_add=True)
    play_summary = models.TextField(null=True)

    class Meta:
        db_table = 'history_play_summary'

    def __str__(self):
        return self.play_summary


class StaffRole(models.Model):
    staff_role_name = models.TextField()
    staff_role_description = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'history_staff_role'

    def __str__(self):
        return self.staff_role_name


class PlayCharacter(models.Model):
    play_character_name  = models.CharField(max_length=100)
    play_character_description = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'history_play_character'

    def __str__(self):
        return self.play_character_name


class PlayScript(models.Model):
    script_name = models.TextField()
    script_author = models.TextField()
    script_member_author = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True)
    script_created = models.DateField(null=True, blank=True)
    script_description = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'history_play_script'

    def __str__(self):
        return self.script_name


class Participation(models.Model):
    play = models.ForeignKey(Play, on_delete=models.CASCADE)
    play_script = models.ForeignKey(PlayScript, on_delete=models.SET_NULL, null=True)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    is_staff = models.BooleanField() # 배우, 스탭
    play_character = models.ForeignKey(PlayCharacter, null=True, on_delete=models.SET_NULL)
    staff_role = models.ForeignKey(StaffRole, null=True, on_delete=models.SET_NULL)

    class Meta:
        db_table = 'history_participation'

    def __str__(self):
        return f"{self.play}:{self.member}"
