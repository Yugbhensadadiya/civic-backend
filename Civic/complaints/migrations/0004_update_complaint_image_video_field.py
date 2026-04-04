from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('complaints', '0003_complainstatushistory_update_status_choices'),
    ]

    operations = [
        migrations.AlterField(
            model_name='complaint',
            name='image_video',
            field=models.ImageField(blank=True, null=True, upload_to='departments/'),
        ),
    ]
