"""
    accounts.profile.serializers
    ============================

    Serializers file for a basic Accounts App

"""
from rest_framework import serializers

from .models import AccountsUser


class AccountsUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = AccountsUser
