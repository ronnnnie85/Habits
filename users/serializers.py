from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ("id", "email", "phone", "tg_id", "password", "avatar")

    def create(self, validated_data):
        # выдергиваем email и password, чтобы не передавать их дважды
        email = validated_data.pop("email")
        password = validated_data.pop("password")

        user = User.objects.create_user(
            email=email,
            password=password,
            **validated_data,  # здесь уже только phone, tg_id, avatar и т.п.
        )
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "phone", "tg_id", "avatar")

    def update(self, instance, validated_data):
        instance.email = validated_data.get("email", instance.email)
        instance.phone = validated_data.get("phone", instance.phone)
        instance.tg_id = validated_data.get("tg_id", instance.tg_id)
        instance.avatar = validated_data.get("avatar", instance.avatar)
        instance.save()
        return instance
