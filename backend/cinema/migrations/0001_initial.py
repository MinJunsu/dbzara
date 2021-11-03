# Generated by Django 3.2.8 on 2021-11-01 17:32

from django.db import migrations, models
import django.db.models.deletion
import psqlextra.backend.migrations.operations.add_default_partition
import psqlextra.backend.migrations.operations.create_partitioned_model
import psqlextra.manager.manager
import psqlextra.models.partitioned
import psqlextra.types


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('item', '0001_initial'),
        ('movie', '0001_initial'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('content', models.TextField()),
                ('attachment', models.ImageField(upload_to='inquiry/%Y/%m')),
            ],
        ),
        migrations.CreateModel(
            name='Cinema',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True, verbose_name='이름')),
                ('address', models.CharField(max_length=50, verbose_name='주소')),
                ('latitude', models.DecimalField(decimal_places=6, max_digits=9, verbose_name='위도')),
                ('longitude', models.DecimalField(decimal_places=6, max_digits=9, verbose_name='경도')),
                ('grade', models.IntegerField(choices=[(1, 'S 등급'), (2, 'A 등급'), (3, 'B 등급'), (4, 'C 등급')])),
            ],
        ),
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(choices=[(4, '신품'), (3, '중고품'), (2, '정비필요품'), (1, '폐품')])),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='제목')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('content', models.TextField(verbose_name='내용')),
                ('attachment', models.ImageField(upload_to='inquiry/%Y/%m')),
            ],
        ),
        migrations.CreateModel(
            name='QuestionCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=100, verbose_name='내용')),
            ],
        ),
        psqlextra.backend.migrations.operations.create_partitioned_model.PostgresCreatePartitionedModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('schedule', models.BigIntegerField()),
                ('order', models.BigIntegerField()),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('reservation_number', models.CharField(max_length=15)),
                ('seat_column', models.IntegerField()),
                ('seat_row', models.IntegerField()),
                ('is_canceled', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            partitioning_options={
                'method': psqlextra.types.PostgresPartitioningMethod['RANGE'],
                'key': ['datetime'],
            },
            bases=(psqlextra.models.partitioned.PostgresPartitionedModel,),
            managers=[
                ('objects', psqlextra.manager.manager.PostgresManager()),
            ],
        ),
        psqlextra.backend.migrations.operations.add_default_partition.PostgresAddDefaultPartition(
            model_name='Reservation',
            name='default',
        ),
        psqlextra.backend.migrations.operations.create_partitioned_model.PostgresCreatePartitionedModel(
            name='Schedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField(unique=True)),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            partitioning_options={
                'method': psqlextra.types.PostgresPartitioningMethod['RANGE'],
                'key': ['datetime'],
            },
            bases=(psqlextra.models.partitioned.PostgresPartitionedModel,),
            managers=[
                ('objects', psqlextra.manager.manager.PostgresManager()),
            ],
        ),
        psqlextra.backend.migrations.operations.add_default_partition.PostgresAddDefaultPartition(
            model_name='Schedule',
            name='default',
        ),
        migrations.CreateModel(
            name='Seat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('columns', models.IntegerField(verbose_name='열')),
                ('rows', models.IntegerField(verbose_name='행')),
            ],
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('manager_name', models.CharField(max_length=50)),
                ('manager_phone_number', models.CharField(max_length=13)),
            ],
        ),
        migrations.CreateModel(
            name='Theater',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=5, verbose_name='이름')),
                ('category', models.CharField(max_length=10, verbose_name='종류')),
                ('floor', models.IntegerField(verbose_name='층')),
                ('cinema', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cinema.cinema', verbose_name='영화관')),
                ('materials', models.ManyToManyField(related_name='_cinema_theater_materials_+', through='cinema.Material', to='item.Item')),
                ('seat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cinema.seat', verbose_name='좌석구조')),
            ],
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('standard_quantity', models.IntegerField()),
                ('quantity', models.IntegerField()),
                ('supply_price', models.IntegerField()),
                ('modified', models.DateTimeField(auto_now=True)),
                ('cinema', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cinema.cinema')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='item.item')),
                ('supplier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cinema.supplier')),
            ],
        ),
        migrations.AddField(
            model_name='schedule',
            name='cinema',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cinema.cinema'),
        ),
        migrations.AddField(
            model_name='schedule',
            name='movie',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movie.movie'),
        ),
        migrations.AddField(
            model_name='schedule',
            name='theater',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cinema.theater'),
        ),
        migrations.AddField(
            model_name='questioncategory',
            name='question_category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cinema.questioncategory'),
        ),
        migrations.AddField(
            model_name='question',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cinema.questioncategory'),
        ),
        migrations.AddField(
            model_name='question',
            name='cinema',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cinema.cinema'),
        ),
        migrations.AddField(
            model_name='question',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.profile'),
        ),
        migrations.AddField(
            model_name='material',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='item.item'),
        ),
        migrations.AddField(
            model_name='material',
            name='theater',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cinema.theater'),
        ),
        migrations.AddField(
            model_name='cinema',
            name='events',
            field=models.ManyToManyField(related_name='cinema', to='item.Event'),
        ),
        migrations.AddField(
            model_name='cinema',
            name='inquiries',
            field=models.ManyToManyField(related_name='_cinema_cinema_inquiries_+', through='cinema.Question', to='accounts.Profile'),
        ),
        migrations.AddField(
            model_name='cinema',
            name='schedules',
            field=models.ManyToManyField(related_name='_cinema_cinema_schedules_+', through='cinema.Schedule', to='movie.Movie'),
        ),
        migrations.AddField(
            model_name='cinema',
            name='stocks',
            field=models.ManyToManyField(related_name='_cinema_cinema_stocks_+', through='cinema.Stock', to='item.Item'),
        ),
        migrations.AddField(
            model_name='answer',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.employee'),
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='cinema.question'),
        ),
    ]
