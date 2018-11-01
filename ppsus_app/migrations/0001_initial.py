# Generated by Django 2.0.2 on 2018-02-14 18:23

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import multiselectfield.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Edmonton',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_inicio', models.DateTimeField(auto_now_add=True)),
                ('data_fim', models.DateTimeField(auto_now=True)),
                ('fragilidade', models.CharField(max_length=1, null=True)),
                ('fatores', models.CharField(max_length=300, null=True)),
                ('q1_cognicao', models.PositiveSmallIntegerField(choices=[(1, 'Aprovado'), (2, 'Reprovado com erros mínimos'), (3, 'Reprovado com erros significantes')])),
                ('q1_foto_relogio', models.ImageField(upload_to='uploads/%Y/%m/%d/')),
                ('q2_estado_saude_A', models.PositiveSmallIntegerField(choices=[(1, '0'), (2, '1 ou 2'), (3, '3 ou +')])),
                ('q2_estado_saude_B', models.PositiveSmallIntegerField(choices=[(1, 'Excelente'), (2, 'Muito boa'), (3, 'Boa'), (4, 'Razoável'), (5, 'Ruim')])),
                ('q3_ind_func', multiselectfield.db.fields.MultiSelectField(choices=[('1', 'Preparar refeição (cozinhar)'), ('2', 'Usar o telefone'), ('3', 'Transporte (se locomover)'), ('4', 'Lavar a roupa'), ('5', 'Cuidar da casa (limpar / arrumar)'), ('6', 'Cuidar do dinheiro'), ('7', 'Fazer compras'), ('8', 'Tomar remédios')], max_length=15)),
                ('q4_sup_social', models.PositiveSmallIntegerField(choices=[(1, 'Sempre'), (2, 'As vezes'), (3, 'Nunca')])),
                ('q5_medicamento_A', models.PositiveSmallIntegerField(choices=[(1, 'Sim'), (2, 'Não')])),
                ('q5_medicamento_B', models.PositiveSmallIntegerField(choices=[(1, 'Sim'), (2, 'Não')])),
                ('q6_nutricao', models.PositiveSmallIntegerField(choices=[(1, 'Sim'), (2, 'Não')])),
                ('q7_humor', models.PositiveSmallIntegerField(choices=[(1, 'Sim'), (2, 'Não')])),
                ('q8_continencia', models.PositiveSmallIntegerField(choices=[(1, 'Sim'), (2, 'Não')])),
                ('q9_desemp_func', models.PositiveSmallIntegerField(choices=[(1, '0-10 segundos'), (2, '11-20 segundos'), (3, '21 segundos ou mais')])),
                ('q9_desemp_func_tempo', models.TimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Paciente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('nro_sus', models.CharField(max_length=15)),
                ('data_nascimento', models.DateField()),
                ('end_bairro', models.CharField(max_length=100, null=True)),
                ('end_rua', models.CharField(max_length=100, null=True)),
                ('end_numero', models.CharField(max_length=100, null=True)),
                ('cep', models.CharField(max_length=8, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Posto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('end_bairro', models.CharField(max_length=100, null=True)),
                ('end_rua', models.CharField(max_length=100, null=True)),
                ('end_numero', models.IntegerField(null=True)),
                ('cep', models.CharField(max_length=8, null=True)),
                ('telefone', models.CharField(max_length=11, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Subjetiva',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_inicio', models.DateTimeField(auto_now_add=True)),
                ('data_fim', models.DateTimeField(auto_now=True)),
                ('fragilidade', models.CharField(max_length=1, null=True)),
                ('fatores', models.CharField(max_length=300, null=True)),
                ('q1_perdeu_peso', models.PositiveSmallIntegerField(choices=[(1, 'Sim'), (2, 'Não'), (3, 'Não sabe'), (4, 'Não respondeu')])),
                ('q1_perdeu_peso_kg', models.FloatField(null=True)),
                ('q2_ativ_fisica', models.PositiveSmallIntegerField(choices=[(1, 'Sim'), (2, 'Não'), (3, 'Não sabe'), (4, 'Não respondeu')])),
                ('q3_red_forca', models.PositiveSmallIntegerField(choices=[(1, 'Sim'), (2, 'Não'), (3, 'Não sabe'), (4, 'Não respondeu')])),
                ('q4_red_caminhada', models.PositiveSmallIntegerField(choices=[(1, 'Sim'), (2, 'Não'), (3, 'Não sabe'), (4, 'Não respondeu')])),
                ('q5_fadiga', models.PositiveSmallIntegerField(choices=[(1, 'Nunca ou raramente'), (2, 'Às vezes'), (3, 'Frequentemente'), (4, 'Sempre')])),
                ('q6_desanimo', models.PositiveSmallIntegerField(choices=[(1, 'Nunca ou raramente'), (2, 'Às vezes'), (3, 'Frequentemente'), (4, 'Sempre')])),
                ('paciente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subjetiva', to='ppsus_app.Paciente')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subjetiva', to=settings.AUTH_USER_MODEL)),
                ('usuario_edit', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subjetiva_edit', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='edmonton',
            name='paciente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='edmonton', to='ppsus_app.Paciente'),
        ),
        migrations.AddField(
            model_name='edmonton',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='edmonton', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='edmonton',
            name='usuario_edit',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='edmonton_edit', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='user',
            name='posto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to='ppsus_app.Posto'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
    ]