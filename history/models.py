from django.db import models


class Member(models.Model):
    member_name = models.CharField(max_length=10)
    member_class = models.IntegerField(null=True)

    class Meta:
        db_table = 'history_member'

    def __str__(self):
        return self.member_name


class PlayType(models.Model):
    play_type_name = models.CharField(max_length=30)

    class Meta:
        db_table = 'history_play_type'

    def __str__(self):
        return self.play_type_name


class Play(models.Model):
    play_name = models.CharField(max_length=50)
    play_date = models.DateField(null=True)
    play_type = models.ForeignKey(PlayType, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'history_play'

    def __str__(self):
        return self.play_name


class StaffRole(models.Model):
    role_name = models.CharField(max_length=20)
    role_description = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'history_staff_role'

    def __str__(self):
        return self.role_name


class MemberRoleMatch(models.Model):
    play = models.ForeignKey(Play, on_delete=models.CASCADE)
    sub_play = models.CharField(max_length=50, null=True, blank=True)
    member = models.ForeignKey(Member, on_delete=models.CASCADE, null=True, blank=True)
    is_actor = models.BooleanField(default=False)
    actor_role = models.CharField(max_length=50, null=True, blank=True)
    actor_description = models.TextField(null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    staff_role = models.ForeignKey(StaffRole, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = 'history_member_role_match'
        constraints = [
            models.UniqueConstraint(fields=['member', 'staff_role'], name='unique_member_staff_role')
        ]

    def __str__(self):
        return f"{self.play}:{self.member}"
