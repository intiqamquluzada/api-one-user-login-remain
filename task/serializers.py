from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        style={"input_type": "password"}, write_only=True, allow_blank=False
    )

    class Meta:
        model = User
        fields = ("email", "password")
        # extra_kwargs = {
        #     "password": {"write_only": True}
        # }

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        user = User.objects.filter(email=email)

        if not user.exists():
            raise serializers.ValidationError({"error": "Bu email yoxdu"})

        user = user.get()

        if not user.check_password(password):
            raise serializers.ValidationError({"error": "Wrong password"})

        return attrs




class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        style={"input_type": "password"}, write_only=True, allow_blank=False
    )

    class Meta:
        model = User
        fields = ("email", "password")


    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"error": "This email already exists"})

        return attrs