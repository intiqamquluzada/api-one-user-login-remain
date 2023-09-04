class Uploader:

    @staticmethod
    def upload_photo(instance, filename):
        return f"something/{instance.slug}/{filename}"