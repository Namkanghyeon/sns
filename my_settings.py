DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': 'sns-project-nam.ccjgcut3axtl.ap-northeast-2.rds.amazonaws.com',
        'PORT': '5432',
        'NAME': 'sns',
        'USER': 'andy0011',
        'PASSWORD': '00000000',
    }
}

AWS_ACCESS_KEY_ID = 'AKIA5TPCZDSPP4IVCEOJ'
AWS_SECRET_ACCESS_KEY = '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'
AWS_S3_REGION_NAME = 'ap-northeast-2'
AWS_STORAGE_BUCKET_NAME = 'sns-project-nam-bucket'
AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_S3_REGION_NAME}.amazonaws.com"
AWS_DEFAULT_ACL = 'public-read'
